# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Optional authenticated text-only FastAPI facade. No API server on import."""
import hmac
import json
import os
from .core import Config,ValidationError,AlFarouqError,require

SAFE_TASKS=frozenset({'text.analyze','arabic.process','nlp.similarity','privacy.redact'})

def create_app(*,client=None,token=None):
    fastapi=require('fastapi','api')
    from fastapi import FastAPI,Request,HTTPException
    from fastapi.concurrency import run_in_threadpool
    from .client import Client
    client=client or Client()
    token=token if token is not None else os.environ.get('ALFAROUQ_API_KEY')
    if not isinstance(token,str) or len(token)<16:raise ValidationError('Set ALFAROUQ_API_KEY to a secret >=16 characters or pass a secret token. Do not put it in source control.')
    app=FastAPI(title='AlFarouq AI',version='0.3.0a1',description='Authenticated local text services; not a clinical/financial decision system.')
    @app.get('/health')
    def health():return {'status':'ok','version':'0.3.0a1'}
    @app.post('/v1/run')
    async def run(request:Request):
        supplied=request.headers.get('Authorization','')
        if not hmac.compare_digest(supplied.encode(),('Bearer '+token).encode()):raise HTTPException(401,'Valid bearer token required')
        size=0;chunks=[];budget=min(client.config.max_input_bytes,2_000_000)
        async for chunk in request.stream():
            size+=len(chunk)
            if size>budget:raise HTTPException(413,'Request too large')
            chunks.append(chunk)
        try:payload=json.loads(b''.join(chunks))
        except (ValueError,UnicodeError):raise HTTPException(422,'Body must be JSON')
        if not isinstance(payload,dict) or not isinstance(payload.get('inputs'),dict) or payload.get('task') not in SAFE_TASKS:raise HTTPException(403,'Only explicitly allowlisted text tasks are exposed')
        try:result=await run_in_threadpool(client.run,payload['task'],**payload['inputs'])
        except AlFarouqError as exc:raise HTTPException(422,str(exc))
        return result.to_dict()
    return app


def schema(*,config):
    from .core import Result
    # Schema inspection uses a documented test-only token and never starts a server.
    return Result('api.schema',{'openapi':create_app(token='schema-inspection-only').openapi()},'fastapi.openapi',['TestClient/schema validation is not public deployment, TLS, rate limiting or a production security audit.'])
