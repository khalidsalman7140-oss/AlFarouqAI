import os
import pytest
from alfarouqai import AI,Model,Config,ValidationError,ConsentRequired


def test_model_gateway_rejects_unsupported_local_claims():
    with pytest.raises(ValidationError,match='Local gateway'):Model('any-giant-model-will-not-fit')
    with pytest.raises(ValidationError):AI('hello',endpoint='http://127.0.0.1:9')
    with pytest.raises(ValidationError):AI('hello',model='smollm2-135m',image='photo.jpg')
    with pytest.raises(ConsentRequired):Model('server-model',backend='compatible',endpoint='http://127.0.0.1:9/v1')('hello')


@pytest.mark.model
@pytest.mark.skipif(os.environ.get('ALFAROUQ_RUN_MODELS')!='1',reason='Explicit real model test opt-in required')
def test_one_line_local_model_and_reusable_session():
    result=AI('What is the capital of France?',model='smollm2-135m',max_new_tokens=24)
    assert 'Paris' in result.data['text']
    with Model('smollm2-135m') as loaded:
        one=loaded('What is the capital of France?',max_new_tokens=24)
        engine=loaded.engine
        two=loaded('Name the capital of France.',max_new_tokens=24)
        assert loaded.engine is engine and 'Paris' in one.data['text'] and two.data['text']
    assert loaded.engine is None


@pytest.mark.model
@pytest.mark.skipif(os.environ.get('ALFAROUQ_RUN_MODELS')!='1',reason='Explicit real reference-server inference required')
def test_one_line_remote_protocol_model_gateway():
    import sys
    from pathlib import Path
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
    from examples.guide_support import model_server
    with model_server() as origin:
        cfg=Config(allow_network=True)
        result=AI('What is the capital of France?',model='reference-smollm',backend='compatible',endpoint=origin+'/v1',config=cfg,max_new_tokens=24)
        assert 'Paris' in result.data['text']
        result=AI('What is the capital of France?',model='reference-smollm',backend='ollama',endpoint=origin,config=cfg)
        assert 'Paris' in result.data['text']
