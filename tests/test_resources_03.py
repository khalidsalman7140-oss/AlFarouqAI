import os
import pytest
from alfarouqai import AI,Model,Config,ValidationError,environment,model_plan


def test_resource_report_and_estimates():
    info=environment();assert info['python'] and 'ram_limit_gib' in info
    report=model_plan(70,precision_bits=16)
    assert 120<report.data['weight_only_gib']<140
    assert report.data['recommendation'] in ('review-local-gpu-fit','review-local-cpu-fit','use-larger-host-or-compatible-endpoint')
    for value in (0,-1,float('nan'),True):
        with pytest.raises(ValidationError):model_plan(value)


@pytest.mark.model
@pytest.mark.skipif(os.environ.get('ALFAROUQ_RUN_MODELS')!='1',reason='Reviewed trained local weights required')
def test_generic_prompt_and_explicit_cpu_device():
    result=AI('What is the capital of France?')
    assert result.task=='local.generate' and 'Paris' in result.data['text']
    result=AI('What is the capital of France?',model='smollm2-135m',device='cpu',max_new_tokens=24)
    assert result.provenance['device']=='cpu' and 'Paris' in result.data['text']
    with Model('smollm2-135m',device='auto') as model:
        assert model('What is the capital of France?',max_new_tokens=24).data['text']


@pytest.mark.model
@pytest.mark.skipif(os.environ.get('ALFAROUQ_RUN_MODELS')!='1',reason='Torch availability/CPU guard test')
def test_cuda_unavailable_is_not_fake_success():
    import torch
    if not torch.cuda.is_available():
        with pytest.raises(ValidationError,match='CUDA is unavailable'):
            AI('hello',model='smollm2-135m',device='cuda')
    else:
        assert torch.cuda.is_available()  # Real GPU generation remains outside this CPU verification.
