# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Local Whisper recognition and explicit system-executable speech synthesis."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from .core import Result, ValidationError, MissingDependency
from .models import prepare


def recognize(*,audio,config,language=None,model_path=None):
    from .media import transcribe
    path=model_path or prepare('whisper-tiny',config=config)
    result=transcribe(audio=audio,config=config,model_path=str(path),language=language)
    result.task='speech.recognize';result.provenance['actual_weight_inference']=True
    return result


def synthesize(*,text,output,config,voice='en-us',speed=150):
    if not isinstance(text,str) or not text.strip() or len(text)>10000:raise ValidationError('Speech text must be 1..10000 characters')
    if not re.fullmatch(r'[A-Za-z0-9_+\-]+',voice) or type(speed)is not int or not 80<=speed<=350:raise ValidationError('Invalid voice/speed')
    exe=shutil.which('espeak-ng') or shutil.which('espeak')
    if not exe:raise MissingDependency('Install optional espeak-ng executable yourself. It is an external GPL program, not bundled or relicensing this project.')
    path=Path(output)
    if path.suffix.lower()!='.wav':raise ValidationError('TTS output must be a new WAV file')
    if path.exists():raise FileExistsError(path)
    with tempfile.TemporaryDirectory() as tmp:
        wav=Path(tmp)/'speech.wav'
        proc=subprocess.run([exe,'-v',voice,'-s',str(speed),'-w',str(wav),'--stdin'],input=text,capture_output=True,text=True,timeout=config.timeout,shell=False)
        if proc.returncode or not wav.is_file():raise ValidationError('Speech synthesis failed: '+proc.stderr[-1000:])
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as out,wav.open('rb') as source:shutil.copyfileobj(source,out)
    from .media import audio_info
    details=audio_info(audio=path,config=config).data
    return Result('speech.synthesize',{'audio_path':str(path),'voice':voice,**details},'espeak-ng.system',['Classical speech synthesis, not neural natural-voice cloning. Voice availability/languages depend on installed executable. External executable license remains independent.'])
