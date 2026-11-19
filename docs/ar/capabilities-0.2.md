# حالة القدرات 0.2.0

[Handbook](handbook-0.2.md) · [Evidence](../../reports/capability-verification-0.2.json)

| Task | Extra | Verification |
|---|---|---|
| `text.analyze` | core/system | actual-local-execution-verified |
| `data.profile` | core/system | actual-local-execution-verified |
| `ml.train` | ml | actual-local-execution-verified |
| `image.analyze` | vision | actual-local-execution-verified |
| `image.objects` | objects | not-actual-inference-verified |
| `video.motion` | vision | actual-local-execution-verified |
| `audio.info` | core/system | actual-local-execution-verified |
| `speech.transcribe` | speech | actual-local-execution-verified |
| `document.read` | documents | actual-local-execution-verified |
| `code.analyze` | core/system | actual-local-execution-verified |
| `security.logs` | core/system | actual-local-execution-verified |
| `iot.analyze` | core/system | actual-local-execution-verified |
| `llm.chat` | core/system | not-actual-inference-verified |
| `local.generate` | local | actual-local-execution-verified |
| `nlp.classify` | local | actual-local-execution-verified |
| `code.generate` | local | actual-local-execution-verified |
| `code.repair` | local | actual-local-execution-verified |
| `code.test` | core/system | actual-local-execution-verified |
| `document.summarize` | local | actual-local-execution-verified |
| `vision.detect` | torchvision | actual-local-execution-verified |
| `vision.classify` | torchvision | actual-local-execution-verified |
| `vision.segment` | torchvision | actual-local-execution-verified |
| `vision.ocr` | core/system | actual-local-execution-verified |
| `video.track` | torchvision | actual-local-execution-verified |
| `speech.recognize` | speech | actual-local-execution-verified |
| `speech.synthesize` | core/system | actual-local-execution-verified |
| `deep.train` | deep | actual-local-execution-verified |
| `data.forecast` | ml | actual-local-execution-verified |
| `data.recommend` | ml | actual-local-execution-verified |
| `security.anomalies` | ml | actual-local-execution-verified |
| `rag.index` | vector | actual-local-execution-verified |
| `rag.search.semantic` | vector | actual-local-execution-verified |
| `rag.answer` | vector | actual-local-execution-verified |
| `agents.llm` | local | actual-local-execution-verified |
| `automation.tick` | core/system | actual-local-execution-verified |
| `iot.mqtt.publish` | iot | actual-local-execution-verified |
| `iot.mqtt.read` | iot | actual-local-execution-verified |
| `robotics.serial` | iot | actual-local-execution-verified |
| `image.generate` | diffusion | not-actual-inference-verified |
| `video.generate` | diffusion | not-actual-inference-verified |

No physical robot, cross-platform cloud execution, universal-quality model or best-library claim is inferred. Experimental image/video adapters and legacy Ollama/HF-object routes are explicitly not actual-inference-verified.
