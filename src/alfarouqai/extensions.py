# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Additive 0.2 registry; original 0.1 handlers are preserved."""
from .core import Capability, Result
from . import language, vision, speech, learning, integrations, generative


def rag_index(*,document,store,config):
    from .documents import document_read
    from .retrieval import VectorStore
    source=document_read(document=document,config=config)
    with VectorStore(store,config=config) as index:count=index.add(source.data['text'],source=str(document))
    return Result('rag.index',{'chunks_added':count,'store':str(store)},'sentence-transformers+sqlite',provenance={'actual_weight_inference':True})

def rag_search(*,query,store,config,k=4):
    from .retrieval import VectorStore
    with VectorStore(store,config=config) as index:result=index.search(query,k=k)
    result.task='rag.search.semantic';return result

def rag_answer(*,question,store,config,model_path=None,k=3,min_score=.2):
    from .retrieval import VectorStore
    with VectorStore(store,config=config) as index:return index.answer(question,k=k,model_path=model_path,min_score=min_score)

def llm_agent(*,goal,inputs_by_task,config,model_path=None,max_steps=1):
    from .client import Client
    from .automation import LLMAgent
    return LLMAgent(client=Client(config),model_path=model_path).run(goal,inputs_by_task=inputs_by_task,max_steps=max_steps)

def tick(*,store,config,now=None):
    from .automation import Scheduler
    from .client import Client
    scheduler=Scheduler(store,client=Client(config))
    try:return scheduler.tick(now=now)
    finally:scheduler.close()


def register_extensions(registry):
    definitions=[
      ('local.generate',language.generate,'Generate text with a local trained causal language model',('prompt',),'local'),
      ('nlp.classify',language.classify,'Classify supplied text by model likelihood of candidate labels',('text','labels'),'local'),
      ('code.generate',language.code_generate,'Generate untrusted Python code suggestions with a local LLM',('prompt',),'local'),
      ('code.repair',language.code_repair,'Suggest a code repair from supplied code and error',('code','error'),'local'),
      ('code.test',integrations.code_test,'Run trusted unittest files with explicit OS-execution consent',('path',),None),
      ('document.summarize',language.summarize_document,'Summarize extracted document text with a local trained LLM',('document',),'local'),
      ('vision.detect',vision.detect,'Detect COCO objects with pretrained TorchVision SSDlite',('image',),'torchvision'),
      ('vision.classify',vision.classify,'Classify images with pretrained MobileNet V3',('image',),'torchvision'),
      ('vision.segment',vision.segment,'Export a semantic class mask with pretrained LRASPP',('image','output'),'torchvision'),
      ('vision.ocr',vision.ocr,'Recognize printed text with installed Tesseract language models',('image',),None),
      ('video.track',vision.track,'Detect objects and associate temporary track IDs across video',('video',),'torchvision'),
      ('speech.recognize',speech.recognize,'Transcribe speech with local CTranslate2 Whisper weights',('audio',),'speech'),
      ('speech.synthesize',speech.synthesize,'Synthesize an audible WAV using external espeak-ng',('text','output'),None),
      ('deep.train',learning.neural_report,'Train and evaluate a real multilayer PyTorch network',('data','target','problem'),'deep'),
      ('data.forecast',learning.forecast,'Fit a linear time trend with chronological validation',('data','column'),'ml'),
      ('data.recommend',learning.recommend,'Recommend unseen items using collaborative cosine similarity',('data','user','user_column','item_column','rating_column'),'ml'),
      ('security.anomalies',learning.anomalies,'Detect multivariate anomalies with IsolationForest',('data','columns'),'ml'),
      ('rag.index',rag_index,'Extract a document and persist multilingual semantic embeddings',('document','store'),'vector'),
      ('rag.search.semantic',rag_search,'Search persisted semantic vectors with FAISS and source offsets',('query','store'),'vector'),
      ('rag.answer',rag_answer,'Generate a source-returning answer from semantic retrieval',('question','store'),'vector'),
      ('agents.llm',llm_agent,'Use a local LLM to rank allowed tools and review actual results',('goal','inputs_by_task'),'local'),
      ('automation.tick',tick,'Run due persisted local jobs once when the caller ticks',('store',),None),
      ('iot.mqtt.publish',integrations.mqtt_publish,'Publish an explicitly approved MQTT message and await broker ACK',('host','topic','message'),'iot'),
      ('iot.mqtt.read',integrations.mqtt_read,'Read real MQTT messages from an explicitly configured broker',('host','topic'),'iot'),
      ('robotics.serial',integrations.serial_exchange,'Exchange bounded data on a caller-approved local serial port',('port',),'iot'),
    ]
    for name,handler,desc,required,extra in definitions:registry.register(Capability(name,handler,desc,required,extra))
    for name,handler,desc in [('image.generate',generative.image_generate,'Experimental local Stable Diffusion integration'),('video.generate',generative.video_generate,'Experimental local CogVideoX integration')]:
        registry.register(Capability(name,handler,desc,('prompt','model_path','output'),'diffusion','adapter-not-runtime-tested'))
