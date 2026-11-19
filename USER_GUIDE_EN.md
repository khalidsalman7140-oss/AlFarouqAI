# AlFarouq AI 0.3.0a1 — User and Developer Guide
Copyright 2026 Khalid Salman, Yemen. AI Solutions Engineering.
Contact: khalidsalman7140@gmail.com. Founder details are owner-supplied.

## 1. Purpose and learning path
A lightweight Python entry point for real text, data, vision, speech, document,
model, agent, industrial and defensive tools. It reduces integration boilerplate
and returns data, backend, warnings and provenance. It is not a universal model,
a quality benchmark, a production safety certification or unlimited compute.
Start with text and export; install an optional engine for your next project.
Use explicit task names and model sessions for reproducible advanced work.

## 2. Install the delivered release
Python 3.10+ is targeted; actual release verification is Python 3.12/Linux/CPU.
Unzip and enter the folder containing pyproject.toml. Do not assume a similarly
named public PyPI package is this release; no public publication happened here.
```bash
python -m venv .venv
# Windows PowerShell: .\.\.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
python -m alfarouqai --version
```

Alternatively install the included `dist/alfarouqai-0.3.0a1-py3-none-any.whl`.
The core has zero mandatory runtime dependencies. Add only what you need:
`python -m pip install '.[nlp,ml]'` for Arabic text projects, `'.[local]'` for
local text models, `'.[torchvision,vision]'` for pretrained vision, or `'.[vector]'`
for semantic search. The authoritative extras are in pyproject.toml. OCR/TTS/MQTT
may need Tesseract plus language packs, espeak-ng or Mosquitto from your OS.
Import never installs packages, downloads weights or silently enables networking.
A managed installer is opt-in and refuses to change the current interpreter.

## 3. First application, output and routing
Save this as app.py, run `python app.py` from Terminal:
```python
from alfarouqai import AI, Client, Config
result = AI("حلل هذا النص", text="الذكاء الاصطناعي يساعد الطلاب.")
print(result.to_dict())
result.export("text-report.json")
client = Client(Config(verbose=True))
print(client.capabilities())
```

Result.data is the payload, backend identifies the engine, warnings state limits,
and provenance records supported execution/source details. Export accepts JSON,
CSV, Markdown, HTML and TXT, refusing overwrite unless explicitly approved.
Config(verbose=True) writes start/done/backend/error type to stderr. Display or
print results yourself in notebooks; not every external engine exposes a progress
percentage. Use Client.plan before execution and Client.run for unambiguous tasks.
Missing training targets, image references and device permissions are not guessed.
A general text prompt may use the local LLM; this does not authorize arbitrary OS
commands or make unsupported natural-language requests executable.

## 4. Models and resource-aware convenience
```python
from alfarouqai import AI, Config, prepare_model, environment, model_plan, Model
print(environment())
print(model_plan(70, precision_bits=4).to_dict())
# Explicitly approves network + weights download; review license/storage first.
cfg = Config(allow_network=True, allow_model_download=True)
prepare_model("smollm2-135m", config=cfg)
result = AI("What is the capital of France?", model="smollm2-135m", device="auto", config=cfg)
print(result.to_dict())
# A reusable model avoids reloading for every call.
with Model("smollm2-135m", config=cfg, device="cpu") as model:
    print(model("Explain Python briefly.").data)
```

The download step requires your deliberate network/weight consent and the model's
license. The small 135M test model is English-first and limited, not a strong Arabic
assistant. The model registry stores revision/file manifests; no weights ship in
this ZIP. Cache defaults to ~/.cache/alfarouqai/models; ALFAROUQ_MODEL_HOME overrides it.
CPU inference and unavailable-CUDA rejection were tested; real GPU inference was
not. Local model directories must be reviewed Transformers causal-LM safetensors
models; arbitrary architectures and remote Python code are not automatically run.
model_plan estimates weight memory and a rough margin, not context/KV/batch fit,
quantization support or multi-GPU deployment. Use smaller weights or an appropriate
server when resources are insufficient. Model with/close releases reusable sessions.

## 5. Hosted and local inference servers
```python
from alfarouqai import AI, Config
# Requires your already running compatible inference server. Not a live-service test.
r = AI("Explain Python briefly.", model="YOUR_SERVER_MODEL",
       backend="compatible", endpoint="http://127.0.0.1:8000/v1",
       config=Config(allow_network=True))
print(r.data)
```

Use backend='ollama' with the appropriate endpoint for your running Ollama server.
Protocol tests used a real-model reference server; the actual Ollama/vLLM daemons
were not installed/exercised. Remote servers need HTTPS and explicit allow_network
and allow_remote. Pass an environment-variable NAME with api_key_env; never put
the secret value in code or Git. Server provisioning, supported models, permissions,
license, GPU costs and rate limits remain your responsibility. No mandatory paid API.

## 6. Editors, notebooks, cloud and phone
VS Code: open the folder, select .venv through Python: Select Interpreter, run app.py.
PyCharm: choose that same existing interpreter. Jupyter: install ipykernel into the
chosen environment and select its kernel. Colab/Kaggle: upload the ZIP or wheel,
unpack, `%pip install /path/to/release.whl`, and change into the source root for the
examples' fixture helpers. Put tokens in notebook Secrets, save outputs before the
ephemeral runtime ends and separately enable a GPU if needed. These are deployment
instructions, not evidence of a tested platform matrix. Not every engine uses GPU.
Hugging Face Spaces preparation is under deploy/huggingface; Codespaces can use the
same Python setup subject to its host limits. Windows/macOS and cloud runtimes were
not actually run during this local verification. On a phone, download/unzip and
read HTML/Markdown, then use a browser-hosted Python runtime or your inference server;
Android native PyTorch/TensorFlow installation is not an advertised tested path.

## 7. Service catalog and working projects
The complete coding reference at ALFAROUQ_AI_COMPLETE_CODING_GUIDE.md contains every
registered capability, exact executed snippets, requirements and real output previews.
It is bilingual in API/code; this English guide explains the surrounding workflow.
Run `python examples/guide/arabic_process.py` from the root for a self-contained
fixture example, then replace the fixture inputs with your own authorized data.
All source snippets come from guide_catalog and are checked by verify_coding_guide.
Fixtures are synthetic educational data, not patient records or real factory events.

Arabic coursework: normalize/tokenize/ISRI, train TF-IDF + LogisticRegression with
an explicit text/label column, predict and persist, explore LDA topics and lexical
similarity. Stemming is not contextual lemmatization; lexical TF-IDF is not semantic
embedding. Deduplication alone does not prevent group/time/author leakage.
Business: profile/clean/group CSV, monthly sales forecasting with temporal validation,
content recommendations, Decimal ledger reconciliation. Forecasts are not guarantees,
and reconciliation is not payment authorization or proven fraud detection.
Manufacturing: sensor summaries, control charts using independent baselines, aligned
reference-image inspection, labeled maintenance classifiers and production summaries.
These are not universal defect detectors, remaining-useful-life estimators, OEE
without necessary inputs, safety control systems or physical hardware validation.
Developers: AST review, read-only SQLite schema analysis, generated code/test suggestions,
a bounded API and trusted-code test execution. The subprocess runner is NOT a sandbox.
Researchers: read/search documents, persistent multilingual vectors, grounded-answer
attempts, source snippets and export. Validate answers yourself; provenance is not
proof of entailment. Scanned PDFs need OCR preprocessing; not all pages auto-OCR.
Institutions: appointment waiting-time/group analysis and approximate PII patterns;
no clinical diagnosis, regulatory compliance or guaranteed anonymization is claimed.

## 8. Capabilities, exact signatures and prerequisites
The following common setup must precede any service block. It uses the delivered
examples package, so run from the source root, not an installed wheel alone.
model_server/broker/modbus_server are local test fixtures; a protocol fixture is not
proof of a vendor daemon or a physical device. PTY serial tests need POSIX/Linux.
```python
from pathlib import Path
import tempfile, threading
from alfarouqai import AI, Client, Config, Scheduler, prepare_model
from examples.guide_support import make_fixtures, media_fixtures, model_server, broker, modbus_server, create_onnx
ROOT = Path.cwd()  # run from the unpacked AlFarouqAI directory
PHOTO = ROOT/'identity/founder/khalid-salman-original.jpg'
workspace = tempfile.TemporaryDirectory()
DATA, OUT = make_fixtures(workspace.name)
ai = Client()

```

### `text.analyze`
Extractive Arabic/English text statistics and summary

Extra: `core/system`. Required: `text`.

```python
text_analyze(*, text, config: 'Config', **kwargs)
```

Executed service block after the common setup below:
```python
result = ai.run('text.analyze', text='الذكاء الاصطناعي يساعد الطلاب. Python helps researchers.')
```

### `data.profile`
Profile a UTF-8 CSV with missing values and numeric statistics

Extra: `core/system`. Required: `data`.

```python
data_profile(*, data, config, **kwargs)
```

Executed service block after the common setup below:
```python
result = ai.run('data.profile', data=DATA/'numeric.csv')
```

### `ml.train`
Train/test a RandomForest with explicit target/problem

Extra: `ml`. Required: `data, target, problem`.

```python
train_report(*, data, target, problem, config, test_size=0.25, seed=42)
```

Executed service block after the common setup below:
```python
result = ai.run('ml.train', data=DATA/'numeric.csv', target='target', problem='classification')
```

### `image.analyze`
Local image statistics and frontal face detection

Extra: `vision`. Required: `image`.

```python
image_analyze(*, image, config, detect_faces=True, **kwargs)
```

Executed service block after the common setup below:
```python
result = ai.run('image.analyze', image=PHOTO)
```

### `image.objects`
General object detection using reviewed local model weights

Extra: `objects`. Required: `image, model_path`.

```python
objects_detect(*, image, model_path, config, **kwargs)
```

**Experimental / actual-weight inference not verified:** Legacy local object adapter; use tested vision.detect when appropriate.

### `video.motion`
Bounded frame-difference motion regions

Extra: `vision`. Required: `video`.

```python
video_motion(*, video, config, min_area=300, max_frames=None, **kwargs)
```

Executed service block after the common setup below:
```python
media_fixtures(DATA, PHOTO)
result = ai.run('video.motion', video=DATA/'clip.avi', max_frames=3)
```

### `audio.info`
PCM WAV metadata

Extra: `core/system`. Required: `audio`.

```python
audio_info(*, audio, config, **kwargs)
```

Executed service block after the common setup below:
```python
media_fixtures(DATA, PHOTO)
result = ai.run('audio.info', audio=DATA/'silence.wav')
```

### `speech.transcribe`
Whisper transcription with an explicit local model

Extra: `speech`. Required: `audio`.

```python
transcribe(*, audio, config, model_path=None, language=None, **kwargs)
```

Executed service block after the common setup below:
```python
ai.run('speech.synthesize', text='Hello world. A speech recognition test.', output=OUT/'speech.wav')
result = ai.run('speech.transcribe', audio=OUT/'speech.wav', model_path=str(prepare_model('whisper-tiny')), language='en')
```

### `document.read`
Extract text from TXT/PDF/DOCX/XLSX

Extra: `documents`. Required: `document`.

```python
document_read(*, document, config, **kwargs)
```

Executed service block after the common setup below:
```python
result = ai.run('document.read', document=DATA/'note.txt')
```

### `code.analyze`
Non-executing Python AST and project review

Extra: `core/system`. Required: `see signature`.

```python
code_analyze(*, path=None, code=None, config, **kwargs)
```

Executed service block after the common setup below:
```python
result = ai.run('code.analyze', code='import os\nos.system(command)\n')
```

### `security.logs`
Defensive authentication log analysis

Extra: `core/system`. Required: `path`.

```python
security_logs(*, path, config, **kwargs)
```

Executed service block after the common setup below:
```python
result = ai.run('security.logs', path=DATA/'auth.log')
```

### `iot.analyze`
Offline sensor time-series z-score anomaly flags

Extra: `core/system`. Required: `data, column`.

```python
sensor_analyze(*, data, column, threshold=3.0, config, **kwargs)
```

Executed service block after the common setup below:
```python
result = ai.run('iot.analyze', data=DATA/'sensors.csv', column='temperature')
```

### `llm.chat`
Opt-in Ollama text and supported vision chat

Extra: `core/system`. Required: `prompt`.

```python
chat(*, prompt, config, system=None, image=None, **kwargs)
```

Executed service block after the common setup below:
```python
with model_server() as origin:
    result = Client(Config(allow_network=True, ollama_url=origin, model='reference-smollm')).run('llm.chat', prompt='What is the capital of France?')
```

### `local.generate`
Generate text with a local trained causal language model

Extra: `local`. Required: `prompt`.

```python
generate(*, prompt, config, model_path=None, max_new_tokens=96)
```

Executed service block after the common setup below:
```python
result = ai('Explain Python briefly.', task='local.generate', max_new_tokens=40)
```

### `nlp.classify`
Classify supplied text by model likelihood of candidate labels

Extra: `local`. Required: `text, labels`.

```python
classify(*, text, labels, config, model_path=None)
```

Executed service block after the common setup below:
```python
result = ai.run('nlp.classify', text='The service was excellent.', labels=['positive','negative'])
```

### `code.generate`
Generate untrusted Python code suggestions with a local LLM

Extra: `local`. Required: `prompt`.

```python
code_generate(*, prompt, config, model_path=None, max_new_tokens=160)
```

Executed service block after the common setup below:
```python
result = ai.run('code.generate', prompt='Write a Python function add(a,b).', max_new_tokens=60)
```

### `code.repair`
Suggest a code repair from supplied code and error

Extra: `local`. Required: `code, error`.

```python
code_repair(*, code, error, config, model_path=None, max_new_tokens=160)
```

Executed service block after the common setup below:
```python
result = ai.run('code.repair', code='def add(a,b)\n return a+b', error='missing colon', max_new_tokens=60)
```

### `code.test`
Run trusted unittest files with explicit OS-execution consent

Extra: `core/system`. Required: `path`.

```python
code_test(*, path, config, consent=False)
```

Executed service block after the common setup below:
```python
result = ai.run('code.test', path=DATA/'trusted_tests', consent=True)
```

### `document.summarize`
Summarize extracted document text with a local trained LLM

Extra: `local`. Required: `document`.

```python
summarize_document(*, document, config, model_path=None, max_new_tokens=128)
```

Executed service block after the common setup below:
```python
result = ai.run('document.summarize', document=DATA/'note.txt', max_new_tokens=50)
```

### `vision.detect`
Detect COCO objects with pretrained TorchVision SSDlite

Extra: `torchvision`. Required: `image`.

```python
detect(*, image, config, threshold=0.4)
```

Executed service block after the common setup below:
```python
result = ai.run('vision.detect', image=PHOTO)
```

### `vision.classify`
Classify images with pretrained MobileNet V3

Extra: `torchvision`. Required: `image`.

```python
classify(*, image, config, top_k=5)
```

Executed service block after the common setup below:
```python
result = ai.run('vision.classify', image=PHOTO, top_k=3)
```

### `vision.segment`
Export a semantic class mask with pretrained LRASPP

Extra: `torchvision`. Required: `image, output`.

```python
segment(*, image, config, output)
```

Executed service block after the common setup below:
```python
result = ai.run('vision.segment', image=PHOTO, output=OUT/'mask.png')
```

### `vision.ocr`
Recognize printed text with installed Tesseract language models

Extra: `core/system`. Required: `image`.

```python
ocr(*, image, config, language='eng', psm=6)
```

Executed service block after the common setup below:
```python
media_fixtures(DATA, PHOTO)
result = ai.run('vision.ocr', image=DATA/'ocr.png', language='eng')
```

### `video.track`
Detect objects and associate temporary track IDs across video

Extra: `torchvision`. Required: `video`.

```python
track(*, video, config, max_frames=30, threshold=0.4)
```

Executed service block after the common setup below:
```python
media_fixtures(DATA, PHOTO)
result = ai.run('video.track', video=DATA/'clip.avi', max_frames=3)
```

### `speech.recognize`
Transcribe speech with local CTranslate2 Whisper weights

Extra: `speech`. Required: `audio`.

```python
recognize(*, audio, config, language=None, model_path=None)
```

Executed service block after the common setup below:
```python
ai.run('speech.synthesize', text='Hello world. A speech recognition test.', output=OUT/'speech.wav')
result = ai.run('speech.recognize', audio=OUT/'speech.wav', language='en')
```

### `speech.synthesize`
Synthesize an audible WAV using external espeak-ng

Extra: `core/system`. Required: `text, output`.

```python
synthesize(*, text, output, config, voice='en-us', speed=150)
```

Executed service block after the common setup below:
```python
result = ai.run('speech.synthesize', text='Hello world.', output=OUT/'speech.wav', voice='en-us')
```

### `deep.train`
Train and evaluate a real multilayer PyTorch network

Extra: `deep`. Required: `data, target, problem`.

```python
neural_report(*, data, target, problem, config, epochs=80, hidden=(32, 16), seed=42)
```

Executed service block after the common setup below:
```python
result = ai.run('deep.train', data=DATA/'numeric.csv', target='target', problem='classification', epochs=30)
```

### `data.forecast`
Fit a linear time trend with chronological validation

Extra: `ml`. Required: `data, column`.

```python
forecast(*, data, column, config, horizon=5)
```

Executed service block after the common setup below:
```python
result = ai.run('data.forecast', data=DATA/'sensors.csv', column='temperature', horizon=3)
```

### `data.recommend`
Recommend unseen items using collaborative cosine similarity

Extra: `ml`. Required: `data, user, user_column, item_column, rating_column`.

```python
recommend(*, data, user, user_column, item_column, rating_column, config, k=5)
```

Executed service block after the common setup below:
```python
result = ai.run('data.recommend', data=DATA/'ratings.csv', user='u1', user_column='user', item_column='item', rating_column='rating')
```

### `security.anomalies`
Detect multivariate anomalies with IsolationForest

Extra: `ml`. Required: `data, columns`.

```python
anomalies(*, data, columns, config, contamination=0.1)
```

Executed service block after the common setup below:
```python
result = ai.run('security.anomalies', data=DATA/'sensors.csv', columns=['time','temperature'])
```

### `rag.index`
Extract a document and persist multilingual semantic embeddings

Extra: `vector`. Required: `document, store`.

```python
rag_index(*, document, store, config)
```

Executed service block after the common setup below:
```python
result = ai.run('rag.index', document=DATA/'note.txt', store=OUT/'knowledge.sqlite')
```

### `rag.search.semantic`
Search persisted semantic vectors with FAISS and source offsets

Extra: `vector`. Required: `query, store`.

```python
rag_search(*, query, store, config, k=4)
```

Executed service block after the common setup below:
```python
ai.run('rag.index', document=DATA/'note.txt', store=OUT/'knowledge.sqlite')
result = ai.run('rag.search.semantic', query='measuring temperature', store=OUT/'knowledge.sqlite')
```

### `rag.answer`
Generate a source-returning answer from semantic retrieval

Extra: `vector`. Required: `question, store`.

```python
rag_answer(*, question, store, config, model_path=None, k=3, min_score=0.2)
```

Executed service block after the common setup below:
```python
ai.run('rag.index', document=DATA/'note.txt', store=OUT/'knowledge.sqlite')
result = ai.run('rag.answer', question='What measures heat?', store=OUT/'knowledge.sqlite', min_score=.1)
```

### `agents.llm`
Use a local LLM to rank allowed tools and review actual results

Extra: `local`. Required: `goal, inputs_by_task`.

```python
llm_agent(*, goal, inputs_by_task, config, model_path=None, max_steps=1)
```

Executed service block after the common setup below:
```python
result = ai.run('agents.llm', goal='Analyze text statistics.', inputs_by_task={'text.analyze':{'text':'Python helps students.'}})
```

### `automation.tick`
Run due persisted local jobs once when the caller ticks

Extra: `core/system`. Required: `store`.

```python
tick(*, store, config, now=None)
```

Executed service block after the common setup below:
```python
scheduler = Scheduler(OUT/'jobs.sqlite')
scheduler.add('one','text.analyze',{'text':'Hello'},run_at=0)
scheduler.close()
result = ai.run('automation.tick', store=OUT/'jobs.sqlite')
```

### `iot.mqtt.publish`
Publish an explicitly approved MQTT message and await broker ACK

Extra: `iot`. Required: `host, topic, message`.

```python
mqtt_publish(*, host, topic, message, config, port=1883, consent=False)
```

Executed service block after the common setup below:
```python
with broker() as port:
    result = Client(Config(allow_network=True)).run('iot.mqtt.publish', host='127.0.0.1', port=port, topic='demo/readings', message={'temperature':24}, consent=True)
```

### `iot.mqtt.read`
Read real MQTT messages from an explicitly configured broker

Extra: `iot`. Required: `host, topic`.

```python
mqtt_read(*, host, topic, config, port=1883, max_messages=1, duration=3)
```

Executed service block after the common setup below:
```python
with broker() as port:
    def publish():
        import time
        time.sleep(.5)
        Client(Config(allow_network=True)).run('iot.mqtt.publish', host='127.0.0.1', port=port, topic='demo/readings', message='24', consent=True)
    thread = threading.Thread(target=publish); thread.start()
    result = Client(Config(allow_network=True)).run('iot.mqtt.read', host='127.0.0.1', port=port, topic='demo/readings', duration=4)
    thread.join()
```

### `robotics.serial`
Exchange bounded data on a caller-approved local serial port

Extra: `iot`. Required: `port`.

```python
serial_exchange(*, port, config, baudrate=9600, read_bytes=128, command=None, consent=False)
```

Executed service block after the common setup below:
```python
import os, select
master, slave = os.openpty()
def device_side():
    if select.select([master],[],[],4)[0]:
        os.read(master,128); os.write(master,b'PONG')
thread=threading.Thread(target=device_side); thread.start()
try:
    result=Client(Config(timeout=2)).run('robotics.serial',port=os.ttyname(slave),command='PING',read_bytes=4,consent=True)
    thread.join()
finally:
    os.close(master); os.close(slave)
```

### `image.generate`
Experimental local Stable Diffusion integration

Extra: `diffusion`. Required: `prompt, model_path, output`.

```python
image_generate(*, prompt, model_path, output, config, steps=20, seed=42, consent=False)
```

**Experimental / actual-weight inference not verified:** Diffusers Stable Diffusion adapter only; actual generation not tested.

### `video.generate`
Experimental local CogVideoX integration

Extra: `diffusion`. Required: `prompt, model_path, output`.

```python
video_generate(*, prompt, model_path, output, config, frames=17, steps=20, seed=42, consent=False)
```

**Experimental / actual-weight inference not verified:** CogVideoX adapter only; actual generation not tested.

### `arabic.process`
Normalize, tokenize and optionally stem Arabic text

Extra: `nlp`. Required: `text`.

```python
process(*, text, config, stem=True)
```

Executed service block after the common setup below:
```python
result = ai.ar('يكتب الطلاب دروس اللغة العربية في المدارس')
```

### `nlp.train`
Train and evaluate a labeled Arabic/multilingual text classifier

Extra: `ml`. Required: `data, text_column, target`.

```python
train_report(*, data, text_column, target, config, seed=42)
```

Executed service block after the common setup below:
```python
model = ai.text_train(data=DATA/'corpus.csv', text_column='text', target='label')
result = model.report
print(model.predict(['خدمة ممتازة رائعة']).to_dict())
```

### `nlp.topics`
Discover exploratory corpus topics using LDA

Extra: `ml`. Required: `data, text_column`.

```python
topics(*, data, text_column, config, n_topics=3, top_words=8)
```

Executed service block after the common setup below:
```python
result = ai.run('nlp.topics', data=DATA/'corpus.csv', text_column='text', n_topics=2)
```

### `nlp.similarity`
Rank text passages by lexical character TF-IDF similarity

Extra: `ml`. Required: `texts, query`.

```python
similarity(*, texts, query, config, k=5)
```

Executed service block after the common setup below:
```python
result = ai.run('nlp.similarity', texts=['تعلم بايثون','صيانة مضخة'], query='بايثون')
```

### `sales.forecast`
Aggregate calendar months and forecast sales using temporal baselines

Extra: `ml`. Required: `data`.

```python
sales_forecast(*, data, config, date_column=None, value_column=None, horizon=1)
```

Executed service block after the common setup below:
```python
result = ai.sales(DATA/'sales.csv', horizon=1)
```

### `data.clean`
Trim fields and remove exact duplicate CSV rows for review

Extra: `core/system`. Required: `data`.

```python
clean(*, data, config)
```

Executed service block after the common setup below:
```python
result = ai.run('data.clean', data=DATA/'appointments.csv')
```

### `data.group`
Aggregate operational records by an explicit grouping column

Extra: `core/system`. Required: `data, group_column`.

```python
group_data(*, data, group_column, config, value_column=None)
```

Executed service block after the common setup below:
```python
result = ai.run('data.group', data=DATA/'appointments.csv', group_column='department', value_column='waiting_minutes')
```

### `privacy.redact`
Mask email/phone patterns without pretending full anonymization

Extra: `core/system`. Required: `text`.

```python
redact(*, text, config)
```

Executed service block after the common setup below:
```python
result = ai.run('privacy.redact', text='Contact person@example.org +967 700 123 456')
```

### `finance.reconcile`
Reconcile two keyed ledgers using exact decimal amounts

Extra: `core/system`. Required: `left, right, key, amount_column`.

```python
reconcile(*, left, right, key, amount_column, config, tolerance=0.01)
```

Executed service block after the common setup below:
```python
result = ai.run('finance.reconcile', left=DATA/'left.csv', right=DATA/'right.csv', key='id', amount_column='amount')
```

### `industry.sensors`
Extract vibration/sensor statistics and explicitly sampled spectra

Extra: `ml`. Required: `data, columns`.

```python
sensors(*, data, columns, config, sample_rate=None)
```

Executed service block after the common setup below:
```python
result = ai.run('industry.sensors', data=DATA/'sensors.csv', columns=['temperature'], sample_rate=1)
```

### `industry.control`
Screen measurements against separate baseline control limits

Extra: `core/system`. Required: `data, column, baseline`.

```python
control(*, data, column, baseline, config, sigma=3.0)
```

Executed service block after the common setup below:
```python
result = ai.run('industry.control', data=DATA/'sensors.csv', baseline=DATA/'baseline.csv', column='temperature')
```

### `industry.production`
Compute production yield, rejects and optional hourly throughput

Extra: `core/system`. Required: `data, total_column, good_column`.

```python
production(*, data, total_column, good_column, config, operating_hours=None)
```

Executed service block after the common setup below:
```python
result = ai.run('industry.production', data=DATA/'production.csv', total_column='total', good_column='good', operating_hours=3)
```

### `industry.maintenance`
Evaluate a supervised maintenance-label classifier on historical data

Extra: `ml`. Required: `data, target`.

```python
maintenance(*, data, target, config)
```

Executed service block after the common setup below:
```python
result = ai.run('industry.maintenance', data=DATA/'numeric.csv', target='target')
```

### `industry.defects`
Locate aligned-reference image differences for quality screening

Extra: `vision`. Required: `image, reference`.

```python
defects(*, image, reference, config, threshold=25, min_area=20, output=None)
```

Executed service block after the common setup below:
```python
media_fixtures(DATA, PHOTO)
result = ai.inspect(DATA/'bad.png', reference=DATA/'good.png', output=OUT/'difference.png')
```

### `database.profile`
Read SQLite schema and row counts without modifying the database

Extra: `core/system`. Required: `database`.

```python
database_profile(*, database, config)
```

Executed service block after the common setup below:
```python
result = ai.run('database.profile', database=DATA/'factory.sqlite')
```

### `code.tests.generate`
Generate untrusted unittest suggestions with syntax diagnostics

Extra: `local`. Required: `code`.

```python
tests_generate(*, code, config, model_path=None, max_new_tokens=160)
```

Executed service block after the common setup below:
```python
result = ai.run('code.tests.generate', code='def add(a,b):\n    return a+b\n', max_new_tokens=80)
```

### `api.schema`
Build the authenticated text API OpenAPI schema

Extra: `api`. Required: `see signature`.

```python
api_schema(*, config)
```

Executed service block after the common setup below:
```python
result = ai.run('api.schema')
```

### `onnx.predict`
Run reviewed local ONNX tensors with the CPU runtime

Extra: `onnx`. Required: `model_path, inputs`.

```python
onnx_predict(*, model_path, inputs, config)
```

Executed service block after the common setup below:
```python
create_onnx(DATA/'double.onnx')
result = ai.run('onnx.predict', model_path=DATA/'double.onnx', inputs={'x':[[2.],[3.]]})
```

### `tensorflow.predict`
Run a reviewed local single-output Keras model

Extra: `tensorflow`. Required: `model_path, inputs`.

```python
tensorflow_predict(*, model_path, inputs, config)
```

Executed service block after the common setup below:
```python
import tensorflow as tf
model=tf.keras.Sequential([tf.keras.layers.Input(shape=(1,)),tf.keras.layers.Dense(1)])
import numpy as np
model.layers[0].set_weights([np.array([[2.]],dtype='float32'),np.array([1.],dtype='float32')])
model.save(DATA/'linear.keras')
result = ai.run('tensorflow.predict', model_path=DATA/'linear.keras', inputs=[[2.]])
```

### `llm.compatible`
Call an explicitly approved OpenAI-compatible optional inference endpoint

Extra: `core/system`. Required: `prompt, endpoint, model`.

```python
compatible_chat(*, prompt, endpoint, model, config, api_key_env=None, max_tokens=80)
```

Executed service block after the common setup below:
```python
with model_server() as origin:
    result = Client(Config(allow_network=True)).run('llm.compatible', prompt='What is the capital of France?', endpoint=origin+'/v1', model='reference-smollm')
```

### `iot.modbus.read`
Read bounded holding registers from an approved local gateway

Extra: `industrial`. Required: `host, address, count`.

```python
modbus_read(*, host, address, count, config, port=502, device_id=1)
```

Executed service block after the common setup below:
```python
with modbus_server() as port:
    result = Client(Config(allow_network=True)).run('iot.modbus.read', host='127.0.0.1', port=port, address=0, count=2)
```

### `document.insights`
Extract text, keywords, dates and an extractive summary from a file

Extra: `documents`. Required: `document`.

```python
document_insights(*, document, config)
```

Executed service block after the common setup below:
```python
result = AI('حلل هذا الملف واستخرج أهم المعلومات', file=DATA/'note.txt')
```

### `document.search`
Search document passages lexically with source references

Extra: `documents`. Required: `document, query`.

```python
document_search(*, document, query, config, k=3)
```

Executed service block after the common setup below:
```python
result = ai.run('document.search', document=DATA/'note.txt', query='Python')
```

### `ai.search`
Solve a bounded unit-cost grid shortest path with A-star

Extra: `core/system`. Required: `grid, start, goal`.

```python
search(*, grid, start, goal, config)
```

Executed service block after the common setup below:
```python
result = AI('astar', grid=[[0,0,0],[0,1,0]], start=[0,0], goal=[1,2])
```


## 9. Troubleshooting and production boundaries
MissingDependency: install the relevant extra in the active interpreter.
ConsentRequired: review/approve the requested network, model, code or device access.
ValidationError: check files, columns and limits; UnsupportedTask: use explicit task.
OOM: close models, isolate sequential workers or use a smaller model/remote endpoint.
Timeout is not a universal CPU/RAM limiter. Do not run untrusted generated code;
-I and subprocess timeouts do not isolate filesystem/network. Protect credentials,
use HTTPS and review data transfer. Treat retrieved documents as untrusted data,
not agent instructions. Review model/dataset licenses independently of framework licenses.

Scheduler needs tick; it does not keep running when the machine stops. AgentTeam is
a bounded DAG and LLMAgent selects from an allowlist, not an unrestricted autonomous
employee. MQTT delivery is not proof of device action. Serial/Modbus used local PTY/
servers only, not real robots/PLCs. API authentication and limits are a starting point,
not a production security audit. Small-model outputs, ASR and vision can be inaccurate.

## 10. Extend, verify, release and license
Add a lazy-import handler returning Result, register Capability, validate inputs and
permissions, write success/failure tests, update examples, run tests and build before
release. Do not break old task names silently. See CONTRIBUTING and the API reference.
run_verification.py uses isolated sequential pytest workers; --installed checks the
built wheel. verify_coding_guide.py executes exact shared examples using prepared
models/system engines. Read the new release report, not a historical 0.1/0.2 report,
for the final observed counts and limits.
The current original-code license is Apache-2.0, reflecting the latest open-source
request. Copyright remains Khalid Salman's, but Apache grants public license rights;
it is not compatible with an absolute no-reuse restriction. Founder identity/photo
and third-party code/weights/datasets retain independent terms. This is not legal
advice. The private owner guide is deliberately excluded from public staging.
Publication helpers are dry-run by default and need owner authentication/approval.
No public GitHub/PyPI/Hugging Face upload occurred here. Google Drive needs your own
OAuth authorization; AI Drive is a different private storage service. No download
script can waive platform subscription rules. The source release is small; pretrained
weights are separately optional and never hidden in the archive.
