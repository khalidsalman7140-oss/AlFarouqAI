# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Explicit-consent, revision-recorded model cache. No weights ship in the wheel."""
from pathlib import Path
import hashlib
import json
import os
import urllib.request
from .core import Config, ConsentRequired, ValidationError, require

CATALOG = {
 'smollm2-135m': {'repo':'HuggingFaceTB/SmolLM2-135M-Instruct','license':'Apache-2.0','purpose':'English-first instruction LLM; not a strong Arabic model','extra':'local'},
 'minilm-multilingual': {'repo':'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2','license':'Apache-2.0','purpose':'Multilingual sentence embeddings, 384 dimensions','extra':'semantic'},
 'whisper-tiny': {'repo':'Systran/faster-whisper-tiny','license':'MIT (original Whisper); review conversion notices','purpose':'Multilingual speech recognition, CTranslate2','extra':'speech'},
 'mobilenet-v3': {'torchvision':'MobileNet_V3_Small_Weights','license':'Review TorchVision weight/dataset terms','purpose':'ImageNet classification','extra':'torchvision'},
 'ssdlite320': {'torchvision':'SSDLite320_MobileNet_V3_Large_Weights','license':'Review TorchVision weight/COCO data terms','purpose':'COCO object detection','extra':'torchvision'},
 'lraspp': {'torchvision':'LRASPP_MobileNet_V3_Large_Weights','license':'Review TorchVision weight/COCO/VOC terms','purpose':'21-class semantic image segmentation','extra':'torchvision'},
}

def cache_root():
    return Path(os.environ.get('ALFAROUQ_MODEL_HOME', Path.home()/'.cache'/'alfarouqai'/'models'))

def inventory():
    return {name:{**entry,'cached':(cache_root()/name/'alfarouq-model.json').exists()} for name,entry in CATALOG.items()}

def _hash(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def prepare(name, *, config=None, consent=False):
    config=config or Config()
    if name not in CATALOG:raise ValidationError(f'Unknown model {name}; inspect models.inventory()')
    root=cache_root()/name
    marker=root/'alfarouq-model.json'
    if marker.exists():
        record=json.loads(marker.read_text())
        if record.get('model')!=name or any(not (root/f['name']).is_file() or (root/f['name']).stat().st_size!=f['bytes'] for f in record['files']):
            raise ValidationError('Incomplete model cache; review and remove its directory before re-downloading')
        return root
    if not ((consent or config.allow_model_download) and config.allow_network):
        raise ConsentRequired(f'Model {name} not cached. Review {CATALOG[name]}. Call models.prepare(name, config=Config(allow_network=True), consent=True), or approve allow_network and allow_model_download. No download occurred.')
    root.mkdir(parents=True,exist_ok=True)
    entry=CATALOG[name]
    if 'repo' in entry:
        hub=require('huggingface_hub',entry['extra'])
        info=hub.model_info(entry['repo'])
        revision=info.sha
        allow=['*.json','*.txt','*.model','*.safetensors','*.bin','1_Pooling/*','README.md','LICENSE*']
        # No Python remote code, legacy PyTorch pickle, ONNX duplicates or optimizer data.
        names=[f.rfilename for f in info.siblings]
        import fnmatch
        selected=[n for n in names if any(fnmatch.fnmatch(n,p) for p in allow) and not any(t in n for t in ('pytorch_model.bin','training_args','optimizer','onnx/','openvino/','tf_model','flax_model'))]
        for name_in_repo in selected:
            # snapshot_download can fail on proxies that strip Content-Length; use a
            # bounded streaming HTTPS file transfer of the same immutable revision.
            target=root/name_in_repo;target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():continue
            url=f'https://huggingface.co/{entry["repo"]}/resolve/{revision}/{name_in_repo}?download=true'
            request=urllib.request.Request(url,headers={'User-Agent':'AlFarouqAI/0.2.0'})
            temp=target.with_name(target.name+'.partial')
            count=0
            try:
                with urllib.request.urlopen(request,timeout=max(config.timeout,120)) as response,temp.open('wb') as out:
                    while True:
                        block=response.read(1024*1024)
                        if not block:break
                        count+=len(block)
                        if count>1_500_000_000:raise ValidationError('Single model file exceeds 1.5GB download budget')
                        out.write(block)
                temp.replace(target)
            finally:temp.unlink(missing_ok=True)
    else:
        tv=require('torchvision','torchvision')
        group=tv.models.detection if name=='ssdlite320' else tv.models.segmentation if name=='lraspp' else tv.models
        weights=getattr(group,entry['torchvision']).DEFAULT
        revision=weights.url
        target=root/'weights.pth';temp=root/'weights.partial'
        try:
            with urllib.request.urlopen(weights.url,timeout=max(config.timeout,120)) as response,temp.open('wb') as out:
                import shutil
                shutil.copyfileobj(response,out)
            temp.replace(target)
        finally:temp.unlink(missing_ok=True)
        # TorchVision embeds an SHA256 prefix in its official weight filename.
        prefix=weights.url.rsplit('-',1)[-1].split('.')[0]
        if not _hash(target).startswith(prefix):
            target.unlink();raise ValidationError('TorchVision weight hash-prefix mismatch')
    files=[{'name':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':_hash(p)} for p in sorted(root.rglob('*')) if p.is_file() and p!=marker]
    if not files:raise ValidationError('Model snapshot was empty')
    record={'model':name,'source':entry,'revision':revision,'files':files,'note':'Downloaded by explicit consent, not bundled. SHA256 records bytes, not a guarantee of model safety or legal clearance.'}
    marker.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    return root
