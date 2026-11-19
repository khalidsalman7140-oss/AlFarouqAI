# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Bounded cooperative tool agents: planner, specialists, schema reviewer.

This is a deterministic DAG executor, not an autonomous general intelligence.
References are structured Ref objects, not evaluated strings or generated code.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from .core import Result, ValidationError, ConsentRequired


@dataclass(frozen=True)
class Ref:
    step: str
    key: str  # dot-separated Result.data dictionary keys; never attribute evaluation


@dataclass
class Step:
    id: str
    task: str
    inputs: dict = field(default_factory=dict)
    depends_on: tuple[str, ...] = ()
    agent: str = 'specialist'


def references(value):
    if isinstance(value, Ref):
        return {value.step}
    if isinstance(value, dict):
        return set().union(*(references(v) for v in value.values())) if value else set()
    if isinstance(value, (list, tuple)):
        return set().union(*(references(v) for v in value)) if value else set()
    return set()


def resolve(value, results):
    if isinstance(value, Ref):
        if value.step not in results:
            raise ValidationError(f'Unresolved step reference: {value.step}')
        data = results[value.step].data
        for part in value.key.split('.'):
            if not isinstance(data, dict) or part not in data:
                raise ValidationError(f'Invalid result reference {value.step}.{value.key}')
            data = data[part]
        return data
    if isinstance(value, dict):
        return {k: resolve(v, results) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve(v, results) for v in value]
    if isinstance(value, tuple):
        return tuple(resolve(v, results) for v in value)
    return value


class AgentTeam:
    DEFAULT_ALLOWED = frozenset({'text.analyze', 'data.profile', 'ml.train', 'image.analyze', 'video.motion', 'audio.info', 'document.read', 'code.analyze', 'security.logs', 'iot.analyze'})

    def __init__(self, client=None, *, allowed_tasks=None, workers=1):
        from .client import Client
        self.client = client or Client()
        self.allowed = frozenset(allowed_tasks) if allowed_tasks is not None else self.DEFAULT_ALLOWED
        if not isinstance(workers, int) or not 1 <= workers <= 4:
            raise ValidationError('workers must be 1..4')
        self.workers = workers

    def plan(self, steps):
        if not steps or len(steps) > self.client.config.max_agent_steps:
            raise ValidationError('Workflow is empty or exceeds step budget')
        ids = [s.id for s in steps]
        if len(set(ids)) != len(ids) or any(not isinstance(i, str) or not i for i in ids):
            raise ValidationError('Step IDs must be unique nonempty strings')
        dependencies = {}
        for s in steps:
            if s.task not in self.allowed:
                raise ConsentRequired(f'Tool {s.task} is not allowlisted for this team')
            self.client.registry.get(s.task)
            deps = set(s.depends_on) | references(s.inputs)
            if not deps <= set(ids) or s.id in deps:
                raise ValidationError(f'Invalid dependencies for {s.id}')
            dependencies[s.id] = deps
        levels, done = [], set()
        while len(done) < len(steps):
            ready = [s.id for s in steps if s.id not in done and dependencies[s.id] <= done]
            if not ready:
                raise ValidationError('Workflow dependency cycle detected')
            levels.append(ready)
            done.update(ready)
        return levels

    def run(self, steps):
        levels = self.plan(steps)  # Validate the full graph before executing any tool.
        by_id = {s.id: s for s in steps}
        results, trace = {}, [{'agent': 'planner', 'event': 'validated', 'levels': levels}]
        def execute(step):
            return self.client.run(step.task, **resolve(step.inputs, results))
        for level in levels:
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                futures = {sid: pool.submit(execute, by_id[sid]) for sid in level}
                completed = {sid: future.result() for sid, future in futures.items()}
            # Results are only shared after the whole dependency level completes.
            for sid in level:
                result = completed[sid]
                if not isinstance(result.data, dict) or result.task != by_id[sid].task:
                    raise ValidationError(f'Reviewer rejected result schema/task for {sid}')
                import json
                try:
                    json.dumps(result.to_dict(), allow_nan=False)
                except (TypeError, ValueError) as exc:
                    raise ValidationError(f'Reviewer rejected non-serializable data for {sid}') from exc
                # Serialization checked; no claim of semantic truth.
                results[sid] = result
                trace.append({'agent': by_id[sid].agent, 'step': sid, 'task': result.task, 'event': 'completed'})
                trace.append({'agent': 'schema-reviewer', 'step': sid, 'event': 'schema-accepted'})
        return Result('agents.workflow', {'results': {sid: r.to_dict() for sid, r in results.items()}, 'trace': trace, 'levels': levels}, 'bounded-dag-agents', ['Deterministic specialist orchestration and schema validation, not independent LLM deliberation or factual verification. Tool execution has no OS sandbox; do not load untrusted plugins.'])
