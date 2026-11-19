# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Dependency-free resource inspection and explicitly approximate model planning."""
from pathlib import Path
import math,os,platform,shutil,subprocess,sys
from .core import Result,ValidationError


def environment():
    memory=None
    try:memory=os.sysconf('SC_PAGE_SIZE')*os.sysconf('SC_PHYS_PAGES')
    except (ValueError,OSError,AttributeError):pass
    for f in ('/sys/fs/cgroup/memory.max','/sys/fs/cgroup/memory/memory.limit_in_bytes'):
        try:
            value=int(Path(f).read_text().strip())
            if value>0:memory=min(memory,value) if memory else value
        except (OSError,ValueError):pass
    gpu=[];exe=shutil.which('nvidia-smi')
    if exe:
        try:
            p=subprocess.run([exe,'--query-gpu=memory.total,memory.free','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=5,shell=False)
            if p.returncode==0:
                for line in p.stdout.splitlines():
                    total,free=map(float,line.split(','));gpu.append({'total_gib':round(total/1024,3),'free_gib':round(free/1024,3)})
        except (OSError,ValueError,subprocess.TimeoutExpired):pass
    kind='colab' if 'COLAB_RELEASE_TAG' in os.environ or 'COLAB_GPU' in os.environ else 'kaggle' if 'KAGGLE_KERNEL_RUN_TYPE' in os.environ else 'codespaces' if os.environ.get('CODESPACES')=='true' else 'huggingface-space' if 'SPACE_ID' in os.environ else 'local-or-unspecified'
    return {'python':sys.version.split()[0],'system':platform.system(),'machine':platform.machine(),'logical_cpus':os.cpu_count(),'ram_limit_gib':round(memory/1024**3,3) if memory else None,'nvidia_gpus':gpu,'environment_hint':kind,'note':'Environment hints are not platform validation. RAM limit is not current free RAM; nvidia-smi availability does not prove framework compatibility.'}


def model_plan(parameters_billion,*,precision_bits=16):
    if isinstance(parameters_billion,bool) or not isinstance(parameters_billion,(int,float)) or not math.isfinite(parameters_billion) or parameters_billion<=0 or precision_bits not in (4,8,16,32):raise ValidationError('Positive finite parameter billions and precision_bits in 4/8/16/32 required')
    info=environment();weight_gib=parameters_billion*1_000_000_000*precision_bits/8/1024**3
    estimate=weight_gib*1.35
    best_gpu=max((g['free_gib'] for g in info['nvidia_gpus']),default=0)
    ram=info['ram_limit_gib'] or 0
    recommendation='review-local-gpu-fit' if best_gpu>=estimate else 'review-local-cpu-fit' if ram>=estimate else 'use-larger-host-or-compatible-endpoint'
    return Result('resources.plan',{'resources':info,'weight_only_gib':round(weight_gib,3),'illustrative_runtime_gib':round(estimate,3),'recommendation':recommendation},'stdlib.resource-estimate',['Rough weight-size heuristic, NOT a fit guarantee. KV cache, context length, batch size, architecture, framework, quantization kernels and temporary buffers are not fully modeled. No download/allocation/quantization/offload is performed.'])
