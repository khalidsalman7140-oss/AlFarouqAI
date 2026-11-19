# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""One-call model gateway; convenience does not create RAM, GPU, or model support."""
from dataclasses import replace
from pathlib import Path
from .core import Config,ValidationError

class Model:
    """A reusable callable local model or a caller-approved inference endpoint.

    Local backend supports reviewed Transformers causal-LM directories and the
    curated SmolLM2 model. Arbitrary remote model names are passed to your server,
    which must already support/load them and satisfy its own hardware/license needs.
    """
    def __init__(self,name='smollm2-135m',*,backend='auto',endpoint=None,config=None,api_key_env=None,device='auto'):
        if not isinstance(name,str) or not name:raise ValidationError('Nonempty model name/local directory required')
        if backend not in ('auto','local','ollama','compatible'):raise ValidationError('backend must be auto/local/ollama/compatible')
        if device not in ('auto','cpu','cuda'):raise ValidationError('device must be auto/cpu/cuda')
        self.device=device
        self.name=name;self.endpoint=endpoint;self.config=config or Config();self.api_key_env=api_key_env;self.engine=None
        self.backend=('compatible' if endpoint else 'local') if backend=='auto' else backend
        if self.backend=='local' and name not in ('smollm2-135m','HuggingFaceTB/SmolLM2-135M-Instruct') and not Path(name).is_dir():
            raise ValidationError('Local gateway accepts the curated model or a reviewed local causal-LM directory. For larger models use an appropriate endpoint/backend; arbitrary architectures/downloads are not implied.')
        if self.backend=='compatible' and not endpoint:raise ValidationError('Compatible backend requires an explicit endpoint, e.g. your server /v1 origin')
    def __call__(self,prompt,*,max_new_tokens=96):
        if self.backend=='local':
            from .language import LocalLanguageModel
            if self.engine is None:
                path=None if self.name in ('smollm2-135m','HuggingFaceTB/SmolLM2-135M-Instruct') else self.name
                self.engine=LocalLanguageModel(config=self.config,model_path=path,device=self.device)
            return self.engine.generate(prompt,max_new_tokens=max_new_tokens)
        if self.backend=='ollama':
            from .providers import chat
            config=replace(self.config,model=self.name,ollama_url=self.endpoint or self.config.ollama_url)
            return chat(prompt=prompt,config=config)
        from .engines import compatible_chat
        return compatible_chat(prompt=prompt,endpoint=self.endpoint,model=self.name,config=self.config,api_key_env=self.api_key_env,max_tokens=max_new_tokens)
    def close(self):
        if self.engine is not None:self.engine.close();self.engine=None
    def __enter__(self):return self
    def __exit__(self,*args):self.close()


def model_call(prompt,*,model='smollm2-135m',backend='auto',endpoint=None,config=None,api_key_env=None,max_new_tokens=96,device='auto'):
    with Model(model,backend=backend,endpoint=endpoint,config=config,api_key_env=api_key_env,device=device) as loaded:
        return loaded(prompt,max_new_tokens=max_new_tokens)
