> Preserved 0.1.0 documentation. Current status: [0.2 handbook](handbook-0.2.md) and [0.2 matrix](capabilities-0.2.md).

# User guide
[Home](../../README.md) · [العربية](../ar/guide.md) · [Capability matrix](capabilities.md)

## 1. Install only what you need
Core: Python >=3.10; this delivery is locally tested on Python 3.12/Linux only.
Other platforms/versions are CI targets, not locally verified claims.
Create/activate a virtual environment and run `python -m pip install .` in the
unpacked project, or install the supplied wheel from dist. Build isolation may
fetch setuptools even though runtime dependencies are empty.

| Extra | Install from checkout | Engine and requirements |
|---|---|---|
| ml | `python -m pip install '.[ml]'` | scikit-learn, pandas |
| vision | `python -m pip install '.[vision]'` | OpenCV 4.x, CPU |
| documents | `python -m pip install '.[documents]'` | pypdf, python-docx, openpyxl |
| speech | `python -m pip install '.[speech]'` | faster-whisper; separate CTranslate2 weights |
| semantic | `python -m pip install '.[semantic]'` | SentenceTransformers; separate weights |
| objects | `python -m pip install '.[objects]'` | Transformers, PyTorch, safetensors; separate weights |
| persistence | `python -m pip install '.[persistence]'` | skops; save-only interface |
| dev | `python -m pip install -e '.[dev]'` | tests/build/metadata validation |

No paid service is mandatory. Hardware, power, internet and storage still have
costs. Start with small CPU workloads. There is no single RAM recommendation for
all model architectures; inspect the model card, disk size, quantization and
context requirements. Benchmark quality/latency/memory instead of picking a model
because someone calls it the strongest.

## 2. Beginner, developer and researcher interfaces
```python
from alfarouqai import AI, Client
result = AI('analyze this text', text='Python helps students. Local AI enables research.')
print(result.data['keywords'])
client = Client()
result = client.run('data.profile', data='examples/data/students.csv')
print(client.plan('train a prediction model', data='examples/data/students.csv'))
```
AI is a function returning Result; Client persists configuration/registry.
Routing is a conservative Arabic/English rule system, NOT unrestricted language
understanding. It rejects ambiguous inputs and unsupported semantics instead of
silently giving a weaker operation a stronger name. No installation or download
occurs from calling AI. Use explicit task names for repeatable experiments.

## 3. Tabular training, evaluation and prediction
Run `python examples/02_machine_learning.py` for a complete executable example.
For your own data:
```python
from alfarouqai import Client
model = Client().train(data='your-training.csv', target='label',
                       problem='classification', seed=42)
print(model.report.data['metrics'])
predictions = model.predict([{'feature1':1.5, 'feature2':'category'}])
predictions.export('predictions.csv')
```
This snippet is a schema template for YOUR CSV, not the bundled students CSV.
Specify target and classification/regression explicitly. CSV must have a unique
UTF-8 header, >=12 rows, >=1 feature and no missing labels. Classification needs
>=2 classes with >=2 observations per class AND a valid stratified split.

The random train/test split (default 75/25, seed 42) happens before learned
imputation, scaling and one-hot encoding. Numeric feature typing uses the training
split only. The target is dropped from features; unknown prediction categories
are allowed. Prediction rows must contain exactly the training features.
The estimator is a 60-tree RandomForest, not AutoML or deep learning. Classification
reports accuracy and weighted F1; regression reports MAE and R². Inspect proxy
columns, duplicate leakage and sampling bias yourself. Random splitting is not
appropriate for temporal/grouped/causal evaluations. Synthetic-fixture scores are
not a real-world benchmark.

`Client.run('ml.train',...)` returns only a report; `Client.train(...)` returns the
usable in-memory TrainedModel. Save with `model.save('model.skops',consent=True)`
only after installing persistence. Save inference was not tested in this delivery;
there is no model-load API yet. No untrusted pickle/joblib loading is provided.

## 4. Vision, motion and audio
```python
client.run('image.analyze', image='photo.jpg')
client.run('video.motion', video='clip.avi', max_frames=100, min_area=300)
client.run('audio.info', audio='recording.wav')
```
image.analyze returns dimensions, mean RGB and frontal Haar face boxes, NOT identity
or general objects. video.motion returns frame-difference regions and timestamps,
NOT person/action understanding or persistent tracking. Camera motion can trigger
it. Default maximum is 300 frames and truncation is explicit. Codec support depends
on the installed OpenCV wheel. audio.info handles PCM WAV metadata, not speech.

```python
client.run('image.objects', image='photo.jpg', model_path='/local/reviewed/detector')
client.run('speech.transcribe', audio='speech.wav', model_path='/local/whisper-ct2', language='en')
```
These optional adapters have not been exercised with actual weights in this delivery.
The detector needs a compatible local Transformers object-detection model in
safetensors format. Remote custom code is disabled. Whisper requires a local
CTranslate2 model, runs CPU/int8, and refuses downloads unless the user explicitly
sets allow_model_download=True after license/resource review. No weights are bundled.

## 5. Documents and retrieval
```python
from alfarouqai import Client, KnowledgeBase
client = Client()
doc = client.run('document.read', document='examples/data/knowledge.txt')
kb = KnowledgeBase(chunk_size=800, overlap=100)
kb.add(doc.data['text'], source='knowledge.txt')
print(kb.search('خالد سلمان', k=3).data['rows'])
kb.save('knowledge.json')
restored = KnowledgeBase.load('knowledge.json')
```
KnowledgeBase uses lexical TF-IDF cosine retrieval, not semantic embeddings. Unicode
word tokenization supports Arabic characters but not semantic synonyms or stemming.
Hits retain source and character offsets. No generated answer is fabricated.
`SemanticIndex('/local/reviewed/embedding-model')` provides an optional local
SentenceTransformer add/search adapter; actual-weight inference was not tested.
Generative RAG with grounded answers is a future composition, not a claimed
complete feature. Treat excerpts as untrusted data, never tool instructions.

TXT/MD/CSV/JSON/Python/log text files work in the core. PDF/DOCX/XLSX require their
engines. PDF is text extraction (no OCR); encrypted PDFs are rejected. DOCX reads
paragraphs and tables; XLSX reads cached values, not formula recalculation. Complex
layout, headers, charts and scanned pages are not guaranteed to extract.

## 6. Code, security and recorded IoT
```python
client.run('code.analyze', path='src/alfarouqai')
client.run('code.analyze', code='import os\nos.system(command)\n')
client.run('security.logs', path='examples/data/auth.log')
client.run('iot.analyze', data='examples/data/sensors.csv', column='temperature', threshold=3)
```
AST analysis collects imports/functions/classes and flags selected risky patterns
without running source code. It neither automatically fixes code nor proves safety.
Log rules identify authentication failures only, not a complete threat detector.
Sensor analytics use a univariate z-score on CSV records; no physical devices,
MQTT traffic, robot control or actuator actions are performed.

## 7. Real, bounded specialist workflows
```python
from alfarouqai import AgentTeam, Step, Ref
result = AgentTeam(workers=2).run([
    Step('read','document.read',{'document':'examples/data/knowledge.txt'},agent='reader'),
    Step('summarize','text.analyze',{'text':Ref('read','text')},agent='summarizer'),
])
print(result.data['trace'])
```
The planner validates the complete DAG, step budget and allowlist before running
specialists. Structured Ref values pass actual Result.data; they are not eval'd
code. Independent levels run with up to four threads; later dependencies wait.
The reviewer validates result task/schema, NOT factual truth. This is deterministic
tool orchestration, not independent LLM debate, self-improvement or autonomy.
LLM calls are excluded from the default team allowlist; explicit changes still
respect network consent. Tool failures propagate, not fake success. Plugins and
CPU engines are in-process: they have no hard timeout, memory sandbox or rollback.

## 8. Local LLM and VS Code
Install Ollama outside this project, inspect/download a suitable model yourself,
then opt in to requests to your local server:
```python
from alfarouqai import Client, Config
client = Client(Config(model='YOUR_LOCAL_MODEL', allow_network=True))
print(client.run('llm.chat',prompt='Explain machine learning briefly').data['text'])
```
The transport defaults to loopback, no proxy inheritance and no redirects. Network
is OFF even for loopback unless explicitly allowed. Remote use additionally needs
allow_remote=True AND HTTPS. Verify that your server/model alias does not route
to a cloud service; a local origin alone cannot prove local inference. The -cloud
suffix is blocked but arbitrary server-side aliases cannot be detected. Image input
via llm.chat requires a compatible vision model; not every model supports images.

Open the project folder in VS Code, install the official Python extension, select
your virtual environment with Python: Select Interpreter, then run an example or
use .vscode/launch.json. There is no custom VS Code extension. Normal Python and
Jupyter workflows are supported by the same importable package.

## 9. Results, configuration and errors
```python
from alfarouqai import Client, Config, AlFarouqError
cfg = Config(max_input_bytes=5_000_000, max_video_frames=100)
cfg.save('my-config.json')
try:
    r = Client(Config.load('my-config.json')).run('text.analyze',text='hello')
    r.export('report.html')
except AlFarouqError as exc:
    print(type(exc).__name__,str(exc))
```
Result contains task, data, backend, warnings, provenance and schema_version.
JSON/CSV/MD/HTML/TXT export creates new files; overwrite=True must be explicit.
CSV exports data.rows when present, otherwise key/value fields; formula-looking
strings are prefixed. HTML is escaped. Missing dependencies/consent/invalid input
raise actionable exceptions. Some underlying parser/estimator exceptions can also
propagate; do not assume a universal error envelope. Config.timeout is an HTTP
timeout only, not a universal task deadline.

## 10. Dependency management and CLI
`alfarouq doctor` checks package presence, NOT full version compatibility.
`alfarouq install-extra vision --environment .alfarouq-env` prints a plan only.
`--yes` explicitly authorizes PyPI downloads in a new/managed dedicated venv,
never the current interpreter or an unrelated existing directory. Install this
checkout/wheel into that venv afterwards, and select its interpreter. Packages
installed in a different venv do not magically become available to the running
process. Package downloads and model downloads are separate consents. Installer
safety gates were tested; its network installation success path was not run.

```bash
alfarouq capabilities
alfarouq plan 'analyze data' --inputs '{"data":"examples/data/students.csv"}'
alfarouq run data.profile --inputs '{"data":"examples/data/students.csv"}' --output profile.json
```
Shell quoting varies: PowerShell/Command Prompt may require adjusted JSON escaping;
the Python API is the most portable option. No external publication is performed.
