# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Experimental diffusion adapters. Actual-weight inference NOT verified in 0.2.0.

The release report must not count validation-only tests as image/video inference.
Large local models are user-supplied; no downloads or cloud service are hidden.
"""
from pathlib import Path
from .core import Result, ConsentRequired, ValidationError, require


def _validate(model_path,output,extension,consent):
    if consent is not True:raise ConsentRequired('Experimental local diffusion can require many GB of RAM/VRAM and long CPU time. Review weights/license/hardware; explicitly pass consent=True.')
    root=Path(model_path);path=Path(output)
    if not root.is_dir():raise ValidationError('Provide a reviewed local diffusion model directory; no automatic download')
    if path.exists():raise FileExistsError(path)
    if path.suffix.lower()!=extension:raise ValidationError('Output extension must be '+extension)
    return root,path


def image_generate(*,prompt,model_path,output,config,steps=20,seed=42,consent=False):
    root,path=_validate(model_path,output,'.png',consent)
    if not isinstance(prompt,str) or not prompt.strip() or len(prompt)>4000 or type(steps)is not int or not 1<=steps<=100:raise ValidationError('Bounded nonempty prompt and steps 1..100 required')
    df=require('diffusers','diffusion');torch=require('torch','diffusion')
    pipe=df.StableDiffusionPipeline.from_pretrained(str(root),local_files_only=True,use_safetensors=True,torch_dtype=torch.float32)
    pipe=pipe.to('cpu');pipe.enable_attention_slicing()
    result=pipe(prompt=prompt,num_inference_steps=steps,height=256,width=256,generator=torch.Generator('cpu').manual_seed(seed))
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:result.images[0].save(stream,format='PNG')
    return Result('image.generate',{'image_path':str(path),'seed':seed,'steps':steps},'diffusers.StableDiffusionPipeline',['Experimental adapter: not actual-weight tested in release verification. Review model and safety checker outputs. Not all diffusion architectures are supported.'])


def video_generate(*,prompt,model_path,output,config,frames=17,steps=20,seed=42,consent=False):
    root,path=_validate(model_path,output,'.mp4',consent)
    if not isinstance(prompt,str) or not prompt.strip() or type(frames)is not int or frames not in (9,17,25,33,49) or type(steps)is not int or not 1<=steps<=100:raise ValidationError('Nonempty prompt, supported CogVideoX frame count and bounded steps required')
    df=require('diffusers','diffusion');torch=require('torch','diffusion')
    pipe=df.CogVideoXPipeline.from_pretrained(str(root),local_files_only=True,use_safetensors=True,torch_dtype=torch.float32).to('cpu')
    video=pipe(prompt=prompt,num_frames=frames,num_inference_steps=steps,generator=torch.Generator('cpu').manual_seed(seed)).frames[0]
    utils=require('diffusers.utils','diffusion');path.parent.mkdir(parents=True,exist_ok=True)
    # Export to a temporary sibling and claim final path exclusively.
    import tempfile,shutil
    with tempfile.TemporaryDirectory() as temp:
        staged=Path(temp)/'output.mp4';utils.export_to_video(video,str(staged),fps=8)
        with path.open('xb') as out,staged.open('rb') as src:shutil.copyfileobj(src,out)
    return Result('video.generate',{'video_path':str(path),'frames':len(video),'seed':seed},'diffusers.CogVideoXPipeline',['Experimental adapter: no actual-weight video generation was run in release verification. Large RAM/VRAM requirement; no production guarantee.'])
