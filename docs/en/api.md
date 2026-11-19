# API reference

Signatures generated from actual handlers. Client supplies Config.

[Guide](guide.md) · [Capabilities](capabilities.md)

```python
AI(prompt, *, config=None, **inputs) -> Result
Client(config=None, registry=None)
Client.run(task, **inputs) -> Result
Client.plan(prompt, **inputs) -> dict
Client.train(data=..., target=..., problem=...) -> TrainedModel
Result.export(path, *, overwrite=False) -> Path
KnowledgeBase(chunk_size=800, overlap=100)
AgentTeam(client=None, allowed_tasks=None, workers=1)
```

## `text.analyze`

Extractive Arabic/English text statistics and summary

```python
client.run('text.analyze', text=...)
```

Extra: `core`. Required: `text`.

## `data.profile`

Profile a UTF-8 CSV with missing values and numeric statistics

```python
client.run('data.profile', data=...)
```

Extra: `core`. Required: `data`.

## `ml.train`

Train/test a RandomForest with explicit target/problem

```python
client.run('ml.train', data=..., target=..., problem=..., test_size=0.25, seed=42)
```

Extra: `ml`. Required: `data, target, problem`.

## `image.analyze`

Local image statistics and frontal face detection

```python
client.run('image.analyze', image=..., detect_faces=True)
```

Extra: `vision`. Required: `image`.

## `image.objects`

General object detection using reviewed local model weights

```python
client.run('image.objects', image=..., model_path=...)
```

Extra: `objects`. Required: `image, model_path`.

## `video.motion`

Bounded frame-difference motion regions

```python
client.run('video.motion', video=..., min_area=300, max_frames=None)
```

Extra: `vision`. Required: `video`.

## `audio.info`

PCM WAV metadata

```python
client.run('audio.info', audio=...)
```

Extra: `core`. Required: `audio`.

## `speech.transcribe`

Whisper transcription with an explicit local model

```python
client.run('speech.transcribe', audio=..., model_path=None, language=None)
```

Extra: `speech`. Required: `audio`.

## `document.read`

Extract text from TXT/PDF/DOCX/XLSX

```python
client.run('document.read', document=...)
```

Extra: `documents`. Required: `document`.

## `code.analyze`

Non-executing Python AST and project review

```python
client.run('code.analyze', path=None, code=None)
```

Extra: `core`. Required: `see handler input rules`.

## `security.logs`

Defensive authentication log analysis

```python
client.run('security.logs', path=...)
```

Extra: `core`. Required: `path`.

## `iot.analyze`

Offline sensor time-series z-score anomaly flags

```python
client.run('iot.analyze', data=..., column=..., threshold=3.0)
```

Extra: `core`. Required: `data, column`.

## `llm.chat`

Opt-in Ollama text and supported vision chat

```python
client.run('llm.chat', prompt=..., system=None, image=None)
```

Extra: `core`. Required: `prompt`.

## `local.generate`

Generate text with a local trained causal language model

```python
client.run('local.generate', prompt=..., model_path=None, max_new_tokens=96)
```

Extra: `local`. Required: `prompt`.

## `nlp.classify`

Classify supplied text by model likelihood of candidate labels

```python
client.run('nlp.classify', text=..., labels=..., model_path=None)
```

Extra: `local`. Required: `text, labels`.

## `code.generate`

Generate untrusted Python code suggestions with a local LLM

```python
client.run('code.generate', prompt=..., model_path=None, max_new_tokens=160)
```

Extra: `local`. Required: `prompt`.

## `code.repair`

Suggest a code repair from supplied code and error

```python
client.run('code.repair', code=..., error=..., model_path=None, max_new_tokens=160)
```

Extra: `local`. Required: `code, error`.

## `code.test`

Run trusted unittest files with explicit OS-execution consent

```python
client.run('code.test', path=..., consent=False)
```

Extra: `core`. Required: `path`.

## `document.summarize`

Summarize extracted document text with a local trained LLM

```python
client.run('document.summarize', document=..., model_path=None, max_new_tokens=128)
```

Extra: `local`. Required: `document`.

## `vision.detect`

Detect COCO objects with pretrained TorchVision SSDlite

```python
client.run('vision.detect', image=..., threshold=0.4)
```

Extra: `torchvision`. Required: `image`.

## `vision.classify`

Classify images with pretrained MobileNet V3

```python
client.run('vision.classify', image=..., top_k=5)
```

Extra: `torchvision`. Required: `image`.

## `vision.segment`

Export a semantic class mask with pretrained LRASPP

```python
client.run('vision.segment', image=..., output=...)
```

Extra: `torchvision`. Required: `image, output`.

## `vision.ocr`

Recognize printed text with installed Tesseract language models

```python
client.run('vision.ocr', image=..., language='eng', psm=6)
```

Extra: `core`. Required: `image`.

## `video.track`

Detect objects and associate temporary track IDs across video

```python
client.run('video.track', video=..., max_frames=30, threshold=0.4)
```

Extra: `torchvision`. Required: `video`.

## `speech.recognize`

Transcribe speech with local CTranslate2 Whisper weights

```python
client.run('speech.recognize', audio=..., language=None, model_path=None)
```

Extra: `speech`. Required: `audio`.

## `speech.synthesize`

Synthesize an audible WAV using external espeak-ng

```python
client.run('speech.synthesize', text=..., output=..., voice='en-us', speed=150)
```

Extra: `core`. Required: `text, output`.

## `deep.train`

Train and evaluate a real multilayer PyTorch network

```python
client.run('deep.train', data=..., target=..., problem=..., epochs=80, hidden=(32, 16), seed=42)
```

Extra: `deep`. Required: `data, target, problem`.

## `data.forecast`

Fit a linear time trend with chronological validation

```python
client.run('data.forecast', data=..., column=..., horizon=5)
```

Extra: `ml`. Required: `data, column`.

## `data.recommend`

Recommend unseen items using collaborative cosine similarity

```python
client.run('data.recommend', data=..., user=..., user_column=..., item_column=..., rating_column=..., k=5)
```

Extra: `ml`. Required: `data, user, user_column, item_column, rating_column`.

## `security.anomalies`

Detect multivariate anomalies with IsolationForest

```python
client.run('security.anomalies', data=..., columns=..., contamination=0.1)
```

Extra: `ml`. Required: `data, columns`.

## `rag.index`

Extract a document and persist multilingual semantic embeddings

```python
client.run('rag.index', document=..., store=...)
```

Extra: `vector`. Required: `document, store`.

## `rag.search.semantic`

Search persisted semantic vectors with FAISS and source offsets

```python
client.run('rag.search.semantic', query=..., store=..., k=4)
```

Extra: `vector`. Required: `query, store`.

## `rag.answer`

Generate a source-returning answer from semantic retrieval

```python
client.run('rag.answer', question=..., store=..., model_path=None, k=3, min_score=0.2)
```

Extra: `vector`. Required: `question, store`.

## `agents.llm`

Use a local LLM to rank allowed tools and review actual results

```python
client.run('agents.llm', goal=..., inputs_by_task=..., model_path=None, max_steps=1)
```

Extra: `local`. Required: `goal, inputs_by_task`.

## `automation.tick`

Run due persisted local jobs once when the caller ticks

```python
client.run('automation.tick', store=..., now=None)
```

Extra: `core`. Required: `store`.

## `iot.mqtt.publish`

Publish an explicitly approved MQTT message and await broker ACK

```python
client.run('iot.mqtt.publish', host=..., topic=..., message=..., port=1883, consent=False)
```

Extra: `iot`. Required: `host, topic, message`.

## `iot.mqtt.read`

Read real MQTT messages from an explicitly configured broker

```python
client.run('iot.mqtt.read', host=..., topic=..., port=1883, max_messages=1, duration=3)
```

Extra: `iot`. Required: `host, topic`.

## `robotics.serial`

Exchange bounded data on a caller-approved local serial port

```python
client.run('robotics.serial', port=..., baudrate=9600, read_bytes=128, command=None, consent=False)
```

Extra: `iot`. Required: `port`.

## `image.generate`

Experimental local Stable Diffusion integration

```python
client.run('image.generate', prompt=..., model_path=..., output=..., steps=20, seed=42, consent=False)
```

Extra: `diffusion`. Required: `prompt, model_path, output`.

## `video.generate`

Experimental local CogVideoX integration

```python
client.run('video.generate', prompt=..., model_path=..., output=..., frames=17, steps=20, seed=42, consent=False)
```

Extra: `diffusion`. Required: `prompt, model_path, output`.

## `arabic.process`

Normalize, tokenize and optionally stem Arabic text

```python
client.run('arabic.process', text=..., stem=True)
```

Extra: `nlp`. Required: `text`.

## `nlp.train`

Train and evaluate a labeled Arabic/multilingual text classifier

```python
client.run('nlp.train', data=..., text_column=..., target=..., seed=42)
```

Extra: `ml`. Required: `data, text_column, target`.

## `nlp.topics`

Discover exploratory corpus topics using LDA

```python
client.run('nlp.topics', data=..., text_column=..., n_topics=3, top_words=8)
```

Extra: `ml`. Required: `data, text_column`.

## `nlp.similarity`

Rank text passages by lexical character TF-IDF similarity

```python
client.run('nlp.similarity', texts=..., query=..., k=5)
```

Extra: `ml`. Required: `texts, query`.

## `sales.forecast`

Aggregate calendar months and forecast sales using temporal baselines

```python
client.run('sales.forecast', data=..., date_column=None, value_column=None, horizon=1)
```

Extra: `ml`. Required: `data`.

## `data.clean`

Trim fields and remove exact duplicate CSV rows for review

```python
client.run('data.clean', data=...)
```

Extra: `core`. Required: `data`.

## `data.group`

Aggregate operational records by an explicit grouping column

```python
client.run('data.group', data=..., group_column=..., value_column=None)
```

Extra: `core`. Required: `data, group_column`.

## `privacy.redact`

Mask email/phone patterns without pretending full anonymization

```python
client.run('privacy.redact', text=...)
```

Extra: `core`. Required: `text`.

## `finance.reconcile`

Reconcile two keyed ledgers using exact decimal amounts

```python
client.run('finance.reconcile', left=..., right=..., key=..., amount_column=..., tolerance=0.01)
```

Extra: `core`. Required: `left, right, key, amount_column`.

## `industry.sensors`

Extract vibration/sensor statistics and explicitly sampled spectra

```python
client.run('industry.sensors', data=..., columns=..., sample_rate=None)
```

Extra: `ml`. Required: `data, columns`.

## `industry.control`

Screen measurements against separate baseline control limits

```python
client.run('industry.control', data=..., column=..., baseline=..., sigma=3.0)
```

Extra: `core`. Required: `data, column, baseline`.

## `industry.production`

Compute production yield, rejects and optional hourly throughput

```python
client.run('industry.production', data=..., total_column=..., good_column=..., operating_hours=None)
```

Extra: `core`. Required: `data, total_column, good_column`.

## `industry.maintenance`

Evaluate a supervised maintenance-label classifier on historical data

```python
client.run('industry.maintenance', data=..., target=...)
```

Extra: `ml`. Required: `data, target`.

## `industry.defects`

Locate aligned-reference image differences for quality screening

```python
client.run('industry.defects', image=..., reference=..., threshold=25, min_area=20, output=None)
```

Extra: `vision`. Required: `image, reference`.

## `database.profile`

Read SQLite schema and row counts without modifying the database

```python
client.run('database.profile', database=...)
```

Extra: `core`. Required: `database`.

## `code.tests.generate`

Generate untrusted unittest suggestions with syntax diagnostics

```python
client.run('code.tests.generate', code=..., model_path=None, max_new_tokens=160)
```

Extra: `local`. Required: `code`.

## `api.schema`

Build the authenticated text API OpenAPI schema

```python
client.run('api.schema', )
```

Extra: `api`. Required: `see handler input rules`.

## `onnx.predict`

Run reviewed local ONNX tensors with the CPU runtime

```python
client.run('onnx.predict', model_path=..., inputs=...)
```

Extra: `onnx`. Required: `model_path, inputs`.

## `tensorflow.predict`

Run a reviewed local single-output Keras model

```python
client.run('tensorflow.predict', model_path=..., inputs=...)
```

Extra: `tensorflow`. Required: `model_path, inputs`.

## `llm.compatible`

Call an explicitly approved OpenAI-compatible optional inference endpoint

```python
client.run('llm.compatible', prompt=..., endpoint=..., model=..., api_key_env=None, max_tokens=80)
```

Extra: `core`. Required: `prompt, endpoint, model`.

## `iot.modbus.read`

Read bounded holding registers from an approved local gateway

```python
client.run('iot.modbus.read', host=..., address=..., count=..., port=502, device_id=1)
```

Extra: `industrial`. Required: `host, address, count`.

## `document.insights`

Extract text, keywords, dates and an extractive summary from a file

```python
client.run('document.insights', document=...)
```

Extra: `documents`. Required: `document`.

## `document.search`

Search document passages lexically with source references

```python
client.run('document.search', document=..., query=..., k=3)
```

Extra: `documents`. Required: `document, query`.

## `ai.search`

Solve a bounded unit-cost grid shortest path with A-star

```python
client.run('ai.search', grid=..., start=..., goal=...)
```

Extra: `core`. Required: `grid, start, goal`.

## Errors / الأخطاء

`ValidationError`, `MissingDependency`, `ConsentRequired`, `UnsupportedTask` inherit `AlFarouqError`. Some engine exceptions propagate; check the guide and security policy.

## Model adapter limits / حدود النماذج

See the current capability-verification report for actual trained-weight tests versus experimental/legacy adapter-only paths.
