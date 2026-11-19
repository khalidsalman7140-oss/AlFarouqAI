"""Actual trained-weight tests. Opt in: ALFAROUQ_RUN_MODELS=1 pytest.

No random-weight neural model is counted as pretrained inference. Teaching DL
training tests are separately labeled in test_upgrade.py.
"""
import gc
import json
import os
from pathlib import Path
import pytest
from alfarouqai import Client, Config, VectorStore, LLMAgent

pytestmark=[pytest.mark.model,pytest.mark.skipif(os.environ.get('ALFAROUQ_RUN_MODELS')!='1',reason='Real model tests require explicit opt-in and reviewed cached weights')]
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/v0.2-model-results'

def save(result,name):
    OUT.mkdir(parents=True,exist_ok=True);result.export(OUT/name,overwrite=True)


def test_real_llm_generation_classification_and_code():
    from alfarouqai.language import LocalLanguageModel
    lm=LocalLanguageModel(config=Config())
    r=lm.generate('What is the capital of France?',max_new_tokens=30)
    assert 'paris' in r.data['text'].casefold();save(r,'local-generation.json')
    ranked=lm.rank('I love this excellent and wonderful book.',['positive','negative'])
    assert ranked.data['rows'] and ranked.provenance['actual_weight_inference'];save(ranked,'nlp-classification.json')
    # Verify actual code generation/repair, not correctness of arbitrary generated programs.
    client=Client()
    for task,inputs,name in [
      ('code.generate',{'prompt':'Write a Python function add(a,b) that returns a+b.','max_new_tokens':70},'code-generation.json'),
      ('code.repair',{'code':'def add(a,b)\n return a+b','error':'SyntaxError: expected colon','max_new_tokens':70},'code-repair.json'),
      ('document.summarize',{'document':ROOT/'examples/data/knowledge.txt','max_new_tokens':50},'document-summary.json')]:
        result=client.run(task,**inputs);assert result.data['text'];save(result,name)
    del lm;gc.collect()


def test_real_torchvision_detection_classification_segmentation_and_video(tmp_path):
    import cv2
    client=Client();photo=ROOT/'identity/founder/khalid-salman-original.jpg'
    r=client.run('vision.detect',image=photo,threshold=.3)
    assert r.data['rows'] and any(x['label']=='person' for x in r.data['rows']);save(r,'object-detection.json')
    r=client.run('vision.classify',image=photo,top_k=5)
    assert len(r.data['rows'])==5;save(r,'image-classification.json')
    OUT.mkdir(parents=True,exist_ok=True);mask=OUT/'semantic-mask.png';mask.unlink(missing_ok=True)
    r=client.run('vision.segment',image=photo,output=mask)
    assert mask.is_file() and any(x['label']=='person' for x in r.data['rows']);save(r,'segmentation.json')
    # A short source-derived fixture is genuine decoded video, not a claimed action benchmark.
    frame=cv2.imread(str(photo));frame=cv2.resize(frame,(360,800));video=tmp_path/'founder-fixture.avi'
    writer=cv2.VideoWriter(str(video),cv2.VideoWriter_fourcc(*'MJPG'),5,(360,800));assert writer.isOpened()
    for _ in range(3):writer.write(frame)
    writer.release()
    r=client.run('video.track',video=video,max_frames=3,threshold=.3)
    assert any(x['objects'] for x in r.data['rows']);save(r,'video-tracks.json')
    objects=[x['objects'] for x in r.data['rows'] if x['objects']]
    assert any(x['track_id']==objects[0][0]['track_id'] for x in objects[-1])
    gc.collect()


def test_real_tts_and_whisper_transcription():
    client=Client();OUT.mkdir(parents=True,exist_ok=True);wav=OUT/'speech-fixture.wav';wav.unlink(missing_ok=True)
    r=client.run('speech.synthesize',text='Hello world. This is a speech recognition test.',output=wav,voice='en-us',speed=140)
    assert r.data['duration_seconds']>1;save(r,'speech-synthesis.json')
    r=client.run('speech.recognize',audio=wav,language='en')
    assert r.data['text'] and any(w in r.data['text'].lower() for w in ('hello','world','speech','test'));save(r,'speech-recognition.json')
    gc.collect()


def test_real_semantic_store_persistence_and_grounded_generation(tmp_path):
    path=tmp_path/'knowledge.sqlite'
    with VectorStore(path) as index:
        index.add('المستشعر يقيس درجة الحرارة ويرسل القراءات.',source='temperature')
        index.add('المكتبة البرمجية توحد أدوات الذكاء الاصطناعي.',source='software')
        index.add('A dog is playing in the park.',source='animals')
        r=index.search('measuring temperature',k=2)
        assert r.data['rows'][0]['source']=='temperature';save(r,'crosslingual-semantic-search.json')
    with VectorStore(path) as index:
        r=index.search('قياس الحرارة',k=1);assert r.data['rows'][0]['source']=='temperature'
        r=index.answer('What measures temperature?',k=1,min_score=.1)
        assert r.data['sources'] and r.data['text'];save(r,'rag-answer.json')
    gc.collect()


def test_real_local_llm_planner_and_reviewer():
    agent=LLMAgent()
    r=agent.run('Analyze and summarize this text with word statistics.',inputs_by_task={'text.analyze':{'text':'Local AI helps students. Students learn Python.'},'code.analyze':{'code':'x=1\n'}},max_steps=1)
    assert r.data['trace'] and r.data['review'];save(r,'llm-agent.json')
    # A valid LLM can choose abstention; completed tool count is reported, not faked.
    assert 0<=r.data['completed_tools']<=1
    gc.collect()
