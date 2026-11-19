# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Persisted local jobs and restricted LLM-guided specialist execution."""
import json
import math
import sqlite3
import time
from .core import Config, Result, ValidationError, ConsentRequired

class Scheduler:
    """Caller-driven tick scheduler; no hidden service, thread or remote workflow."""
    SAFE_TASKS=frozenset({'text.analyze','data.profile','code.analyze','security.logs','iot.analyze','document.read'})
    def __init__(self,path,*,client=None):
        from .client import Client
        self.client=client or Client();self.db=sqlite3.connect(path,timeout=20)
        self.db.execute('CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, task TEXT, inputs TEXT, due REAL, status TEXT, result TEXT)');self.db.commit()
    def add(self,id,task,inputs,*,run_at):
        if task not in self.SAFE_TASKS:raise ConsentRequired('Scheduler only supports explicitly allowlisted, non-actuating local tools')
        if not isinstance(id,str) or not id or not isinstance(inputs,dict) or not isinstance(run_at,(int,float)) or not math.isfinite(run_at):raise ValidationError('Valid id, inputs dictionary and finite UNIX run_at required')
        self.client.registry.get(task);raw=json.dumps(inputs,ensure_ascii=False,allow_nan=False)
        if len(raw)>self.client.config.max_input_bytes:raise ValidationError('Job input too large')
        self.db.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?)',(id,task,raw,float(run_at),'pending',None));self.db.commit()
    def tick(self,*,now=None):
        now=time.time() if now is None else float(now);completed=[]
        if not math.isfinite(now):raise ValidationError('Finite now required')
        while True:
            self.db.execute('BEGIN IMMEDIATE')
            job=self.db.execute("SELECT id,task,inputs FROM jobs WHERE status='pending' AND due<=? ORDER BY due,id LIMIT 1",(now,)).fetchone()
            if not job:self.db.commit();break
            self.db.execute("UPDATE jobs SET status='running' WHERE id=?",(job[0],));self.db.commit()
            try:result=self.client.run(job[1],**json.loads(job[2])).to_dict();status='completed'
            except Exception as exc:result={'error':type(exc).__name__,'message':str(exc)};status='failed'
            self.db.execute('UPDATE jobs SET status=?,result=? WHERE id=?',(status,json.dumps(result,ensure_ascii=False),job[0]));self.db.commit();completed.append({'id':job[0],'status':status,'result':result})
        return Result('automation.tick',{'rows':completed},'sqlite.caller-driven-scheduler',['At-most-once job claiming; a crash can leave running jobs unresolved. No daemon, recurrence or background execution is implied.'])
    def jobs(self):return [{'id':r[0],'task':r[1],'due':r[2],'status':r[3]} for r in self.db.execute('SELECT id,task,due,status FROM jobs ORDER BY due')]
    def cancel(self,id):self.db.execute("UPDATE jobs SET status='cancelled' WHERE id=? AND status='pending'",(id,));self.db.commit()
    def close(self):self.db.close()


class LLMAgent:
    """One real local model with planner/specialist/reviewer roles, not separate minds.

    The LLM ranks a bounded candidate set; model output can never create code,
    file paths or new tool names. Inputs are caller-supplied and immutable by LLM.
    """
    SAFE_TASKS=frozenset({'text.analyze','data.profile','code.analyze','document.read','security.logs','iot.analyze'})
    def __init__(self,*,client=None,model_path=None):
        from .client import Client
        self.client=client or Client();self.model_path=model_path
    def run(self,goal,*,inputs_by_task,max_steps=1):
        if type(max_steps)is not int or not 1<=max_steps<=min(4,self.client.config.max_agent_steps):raise ValidationError('max_steps must be 1..4 and within Config step budget')
        if not isinstance(inputs_by_task,dict) or not inputs_by_task or len(inputs_by_task)>10 or not set(inputs_by_task)<=self.SAFE_TASKS:raise ConsentRequired('Only 1..10 explicit safe local tools with caller-provided inputs are allowed')
        # Validate all required keys before loading a model or touching inputs.
        for task,inputs in inputs_by_task.items():
            cap=self.client.registry.get(task)
            if not isinstance(inputs,dict) or any(k not in inputs for k in cap.required):raise ValidationError(f'Missing inputs for {task}')
        from .language import LocalLanguageModel
        with LocalLanguageModel(config=self.client.config,model_path=self.model_path) as lm:
            remaining=list(inputs_by_task);results={};trace=[]
            for n in range(min(max_steps,len(remaining))):
                labels=[self.client.registry.get(task).description for task in remaining]
                # At least two candidate labels for explicit likelihood comparison.
                ranked=lm.rank('Choose the best next action for this user goal: '+goal,labels+['Finish without using another tool'])
                selected=ranked.data['label'];trace.append({'role':'llm-planner','ranking':ranked.data,'step':n})
                if selected=='Finish without using another tool':break
                task=remaining[labels.index(selected)];remaining.remove(task)
                result=self.client.run(task,**inputs_by_task[task]);results[task]=result.to_dict()
                trace.append({'role':'specialist','task':task,'executed':True})
            review=lm.generate('Review these tool results for missing information. Do not claim to have verified external facts. Goal: '+goal+'\nResults: '+json.dumps(results,ensure_ascii=False)[:6000],max_new_tokens=80)
            return Result('agents.llm',{'results':results,'trace':trace,'review':review.data['text'],'completed_tools':len(results)},'local-llm-constrained-planner+tools+reviewer',['Planner and reviewer share one small local model. Roles are not independent trained agents. No arbitrary tool generation/execution; review can be wrong.'],{'actual_weight_inference':True})
