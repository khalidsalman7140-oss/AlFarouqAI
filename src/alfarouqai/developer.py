# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Read-only DB inspection, safe API scaffolding, and untrusted test suggestions."""
from pathlib import Path
import ast
import json
import sqlite3
import time
from .core import Result,ValidationError,input_file


def database_profile(*,database,config):
    p=input_file(database,config).resolve();deadline=time.monotonic()+config.timeout
    connection=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)
    connection.enable_load_extension(False);connection.execute('PRAGMA query_only=ON')
    connection.set_progress_handler(lambda:1 if time.monotonic()>deadline else 0,1000)
    try:
        tables=connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name LIMIT 201").fetchall()
        if len(tables)>200:raise ValidationError('Database table budget exceeded')
        rows=[]
        for (table,) in tables:
            quoted='"'+table.replace('"','""')+'"'
            cols=connection.execute(f'PRAGMA table_info({quoted})').fetchall()
            if len(cols)>2000:raise ValidationError('Column budget exceeded')
            count=connection.execute(f'SELECT count(*) FROM {quoted}').fetchone()[0]
            rows.append({'table':table,'row_count':count,'columns':[{'name':c[1],'type':c[2],'not_null':bool(c[3]),'primary_key_position':c[5]} for c in cols]})
    except sqlite3.DatabaseError as exc:raise ValidationError('Cannot safely inspect this SQLite database: '+str(exc)) from exc
    finally:connection.close()
    return Result('database.profile',{'rows':rows},'sqlite.read-only',['Schema and row counts only; no row values disclosed, SQL repairs, writes or remote DB access. This is not a vulnerability audit.'])


def tests_generate(*,code,config,model_path=None,max_new_tokens=160):
    from .language import generate
    if not isinstance(code,str) or len(code.encode())>config.max_input_bytes:raise ValidationError('Bounded Python source required')
    try:ast.parse(code)
    except SyntaxError as exc:raise ValidationError('Input code is not syntactically valid Python') from exc
    result=generate(prompt='Write Python unittest test cases for the following function. Do not execute it. Return code only.\n'+code,config=config,model_path=model_path,max_new_tokens=max_new_tokens)
    result.task='code.tests.generate'
    content=result.data['text']
    if '```' in content:
        import re
        match=re.search(r'```(?:python)?\s*\n(.*?)```',content,re.S)
        if match:content=match.group(1)
    try:ast.parse(content);syntax=True
    except SyntaxError:syntax=False
    result.data['syntax_valid']=syntax
    result.warnings.append('LLM-generated test suggestions, not validated test coverage or guaranteed assertions. Never execute untrusted suggestions automatically.')
    return result
