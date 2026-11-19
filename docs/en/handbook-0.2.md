# AlFarouq AI 0.2.0 — practical handbook
[Home](../../README.md) · [Preserved 0.1 guide](guide.md) · [العربية](../ar/handbook-0.2.md)

## 1. Incremental, not a rewrite
The original API, tools, tests, examples and founder identity remain. New engines
add trained local inference, neural training, persistent vectors, model-guided
agents and consent-gated device transports. No benchmark establishes superiority
over every library. This is an accessible facade over specialized libraries, not
a replacement for their algorithms, documentation or licenses.

## 2. Lightweight installation and explicit preparation
Create/activate a virtual environment, then install this checkout or supplied wheel:
```bash
python -m pip install .
python -m pip install '.[local]'
python -m pip install '.[torchvision,vision]'
python -m pip install '.[speech]'
python -m pip install '.[vector]'
python -m pip install '.[deep,iot]'
```
Select extras, not all engines. CPU users can install matching CPU-only PyTorch
wheels from the official PyTorch index first to avoid unnecessary CUDA downloads.
Use platform-specific official installation guidance. reports/verified-requirements-0.2.txt
records the tested environment, not a portable hash lock or universal support claim.

`Client.prepare('vision.detect', '.alfarouq-env')` returns a dependency plan;
`consent=True` runs the existing dedicated-managed-venv installer. Install this
project inside that venv afterwards and select its interpreter. A running process
cannot magically import another venv. Imports/ordinary calls never install packages.
The installer's real network success path was tested for the iot extra in a dedicated managed venv, followed by imports using that venv's interpreter.
Tesseract/language packs, espeak-ng and an MQTT broker are independent optional OS
programs, never silently installed by the library or bundled in the original code.

## 3. Reviewed model cache and consent
```python
from alfarouqai import Client, Config
ai = Client(Config(allow_network=True, allow_model_download=True))
```
This explicitly approves downloading curated models at first use. Afterwards,
`Client()` can run cached weights offline. The default cache is
`~/.cache/alfarouqai/models`; the documented ALFAROUQ_MODEL_HOME variable changes it.
`model_inventory()` lists models; `prepare_model(name, ..., consent=True)` prepares
one. Downloads record immutable Hugging Face revision or official TorchVision URL
plus file SHA-256 values. Ordinary cache-presence checks are not continuous full
cryptographic revalidation or a signed publisher authenticity guarantee.

| Model key | Executed trained model | Boundary |
|---|---|---|
| smollm2-135m | SmolLM2-135M-Instruct | English-first, small and fallible; no advanced Arabic claim |
| minilm-multilingual | multilingual MiniLM-L12-v2 | 384-dimensional semantic search, Arabic/English tested |
| whisper-tiny | CTranslate2 Whisper tiny | actual CPU/int8 recognition on synthesized English audio |
| mobilenet-v3 | ImageNet MobileNet V3 Small | limited ImageNet vocabulary |
| ssdlite320 | COCO SSDlite | limited COCO detections, no identity recognition |
| lraspp | LRASPP/VOC labels | 21-class semantic mask, not instance segmentation |

About 847 MB of weights were downloaded for verification, intentionally NOT placed
in the source ZIP. This keeps delivery lightweight; the model sources need no paid
inference API. Review each exact model/data license and any commercial restrictions
before use/redistribution. A framework license is not blanket model/data clearance.

## 4. One or two inference lines after setup
```python
r = ai.run('vision.detect', image='photo.jpg')
r.export('objects.json')
```
Or use task-name shorthand:
```python
from alfarouqai import AI
r = AI('vision.classify', image='photo.jpg')
```
The original conservative bilingual descriptions remain supported. For free text
with an explicitly chosen model engine:
```python
r = ai('Explain gravity briefly.', task='local.generate')
```
The short call does not erase package installation, hardware requirements or
license/device approval. Arbitrary requests to arbitrary libraries are not claimed.

## 5. NLP, content and code
```python
ai.run('local.generate', prompt='Explain a neural network in two sentences.')
ai.run('nlp.classify', text='This book is wonderful.', labels=['positive','negative'])
ai.run('code.generate', prompt='Write a Python function add(a,b).')
ai.run('code.repair', code='def add(a,b)\n return a+b', error='missing colon')
```
Candidate classification uses local LM label likelihood, not a task-finetuned
sentiment classifier; relative scores are not calibrated probabilities. Generation
is genuine but can be incorrect. The default small English model is not a best-model
or Arabic-quality claim. A reviewed local Transformers-compatible model_path can
be supplied, with potentially much larger RAM needs. Local files only, no remote
custom code, safetensors required. Input is capped at 1024 tokens; output is bounded.

Code is a suggestion, not proven correct and not automatically executed or applied
to source files. Use the original code.analyze for static AST review. For TRUSTED
unittest projects only: `ai.run('code.test', path='trusted_tests', consent=True)`.
A child process, -I and timeout are NOT a security sandbox; filesystem/network
privileges remain. Never auto-run unknown/generated code on a host with secrets.

## 6. Vision, OCR and video
```python
ai.run('vision.detect', image='photo.jpg', threshold=0.4)
ai.run('vision.classify', image='photo.jpg', top_k=5)
ai.run('vision.segment', image='photo.jpg', output='mask.png')
ai.run('vision.ocr', image='scan.png', language='ara+eng')
ai.run('video.track', video='clip.mp4', max_frames=30)
```
The saved PNG contains numeric semantic class IDs, not a retouched photograph.
The tracker combines actual pretrained detections with greedy centroid association
and temporary IDs; crossings/occlusion can swap IDs. No biometric identity or action
understanding is inferred. Tesseract needs relevant system language packs. English
and Arabic printed-fixture OCR ran successfully; this is not a handwriting or
poor-scan accuracy benchmark. Original image.analyze/video.motion remain available.

## 7. Speech in both directions
```python
ai.run('speech.synthesize', text='Hello world.', output='speech.wav', voice='en-us')
ai.run('speech.recognize', audio='speech.wav', language='en')
```
TTS is actual classical espeak-ng synthesis, NOT neural voice cloning. STT is real
Whisper inference. The test transcription misrecognized the start of the synthetic
utterance: execution success does not mean perfect accuracy. Arabic speech accuracy
still needs dedicated tests/human evaluation. PyAV 19 was found incompatible with
the tested faster-whisper path; speech now declares av>=11,<16 and was rerun.

## 8. Actual deep/tabular learning
The original sklearn pipeline remains. New CPU PyTorch MLP training:
```python
model = ai.deep_train(data='numeric.csv', target='label', problem='classification')
model.predict([{'x':1.0, 'y':2.0}]).export('prediction.json')
```
The feature names are YOUR dataset schema. Inputs must be finite numeric values,
with explicit classification/regression. Training-only scaling follows held-out
splitting. hidden and epochs control the network. This is an actual multilayer
network, not generic CNN/Transformer training or LLM finetuning. Save to a new
directory with model.save(...); restore with NeuralModel.load(...,config=Config()).
Weights use safetensors plus JSON. Small synthetic-fixture metrics are not research
generalization evidence. Temporal/grouped data still need domain-aware evaluation.

## 9. Forecasting, recommendation and defensive anomalies
```python
ai.run('data.forecast', data='series.csv', column='temperature', horizon=5)
ai.run('data.recommend', data='ratings.csv', user='u1', user_column='user', item_column='item', rating_column='rating')
ai.run('security.anomalies', data='metrics.csv', columns=['bytes','connections'])
```
Forecasting is a linear-trend baseline with chronological 80/20 validation, not ARIMA,
seasonality or causality. Recommendations use small-data user-cosine collaborative
filtering and have no cold-start/fairness guarantee. IsolationForest anomalies do
not prove an attack. The defensive log/AST tools remain, with no automatic network
scanning or offensive exploitation capability.

## 10. Documents, semantic memory and RAG
```python
ai.run('rag.index', document='notes.pdf', store='knowledge.sqlite')
ai.run('rag.answer', question='What measures temperature?', store='knowledge.sqlite')
```
For control use VectorStore directly:
```python
from alfarouqai import VectorStore
with VectorStore('knowledge.sqlite') as db:
    db.add('المستشعر يقيس درجة الحرارة.', source='lesson')
    hits = db.search('measuring temperature')
```
Trained multilingual embeddings, real FAISS IndexFlatIP and persistent SQLite store
source names/offsets. Index reconstruction uses JSON vectors, not pickle object
loading. The limit is 10000 chunks, not a distributed billion-vector database.
Embedding identity follows model revision/digest, not the cache's machine-specific
path. RAG returns evidence and can abstain below a retrieval threshold, but factual
entailment/citation correctness is NOT guaranteed. Source instructions remain
untrusted. document.summarize reads only a bounded excerpt; no complete long-book
comprehension is claimed. Automatic OCR of scanned PDF is not implemented. Original
KnowledgeBase/SemanticIndex are preserved.

## 11. Model-guided agents and durable caller-driven jobs
```python
from alfarouqai import LLMAgent
r = LLMAgent(client=ai).run('Analyze this text', inputs_by_task={'text.analyze':{'text':'Hello world.'}})
```
The planner ranks only caller-supplied safe tools; a specialist actually executes
the selection; an LLM reviewer comments. Roles share one model, not independent
minds/models. The model cannot invent executable code, tool names, paths or shell
commands. Maximum four steps; abstention is valid. Deterministic AgentTeam remains
better suited to reproducible DAG workflows. Reviews can be wrong.

```python
from alfarouqai import Scheduler
s = Scheduler('jobs.sqlite'); s.add('job1','text.analyze',{'text':'Hello'},run_at=0)
s.tick()
```
No work happens without tick; no hidden daemon or uptime claim. SQLite preserves
states; claims are at-most-once, not exactly-once crash recovery. Running jobs can
remain unresolved after a crash. Network/device tools are excluded. Call s.close().

## 12. Real transports, not physical-robot claims
```python
ai.run('iot.mqtt.read', host='127.0.0.1', topic='sensors/temperature')
ai.run('robotics.serial', port='/dev/ttyUSB0', command='STATUS\n', read_bytes=128, consent=True)
```
MQTT needs allow_network. Remote brokers also need allow_remote and TLS; publish
needs consent=True because messages may trigger actuators. Autonomous defaults
cannot publish/control hardware. Verification used a real local Mosquitto broker
and an actual Linux kernel pseudo-terminal for Serial reads/writes, not physical
sensors or robots. No wiring, actuation, SLAM, navigation or safety certification is
claimed. Review the actual device protocol and safety controls before connecting.

## 13. Image/video synthesis stays experimental
image.generate wraps StableDiffusionPipeline; video.generate wraps CogVideoX.
Only parameter/consent gates were tested: **no actual-weight diffusion inference**
ran for these adapters. They require user-reviewed local model_path, explicit
consent=True and much larger resources. No random-weight output is passed off as
useful generation. Not every Diffusers version/architecture/performance combination
is verified; do not rely on these as production-tested features.

## 14. Verification, exports and portability
Run pytest for ordinary regressions. Actual-weight tests require
ALFAROUQ_RUN_MODELS=1 and prepared model caches. Full local results are in
reports/pytest-0.2.xml and the delivery report. Do not confuse local testing with
remote GitHub Actions, Colab or Kaggle execution: those platforms were NOT run.
Notebook sources and a Hugging Face demo template are prepared for user-approved
upload; no fictional repository URL or automatic publication is included.

All ordinary capabilities return exportable Result objects. Actual outputs under
reports/v0.2-model-results include audio, segmentation mask and model reports.
Model provenance is copied to reports/model-manifests without weight binaries.
Close a SQLite store or use a consistent backup before copying an active database.

## 15. Ownership, adoption and scientific reporting
All original project work/identity is proprietary to Khalid Salman of Yemen. No
public rights to copying, quotation, reuse, modification, derivatives or distribution
are granted without written permission. External frameworks/weights retain separate
licenses. Nothing was publicly published during this task.
This restriction is a material barrier to frictionless worldwide library adoption;
we cannot simultaneously forbid public use and claim a freely reusable ecosystem.
The owner may issue written educational/commercial permissions without surrendering
ownership; the assistant cannot issue permissions on his behalf.

Measure cold-start and warm-inference time separately, publish reproducible task
benchmarks after approval, build Arabic teaching examples, document limitations,
and respect original model citations/data rights. No library can credibly guarantee
first place globally or rapid adoption. In research record model revision/digest,
seed, environment, dataset and evaluation boundaries, not just this wrapper's name.
