> Preserved 0.1.0 documentation. Current status: [0.2 handbook](handbook-0.2.md) and [0.2 matrix](capabilities-0.2.md).

# Capability coverage and roadmap
[العربية](../ar/capabilities.md) · [Guide](guide.md)

Tested means an engine actually ran on local fixtures, not that a general quality
claim was established. See reports/pytest.xml and the final report.

| Requested area | 0.1.0 delivery | Verification / boundary |
|---|---|---|
| NLP | frequency statistics and extractive summary | tested; not neural translation or sentiment |
| LLM | Ollama chat adapter | HTTP contract tested only; no model inference |
| Computer vision | dimensions/colors/Haar faces | tested on supplied photo; not identity |
| IoT | recorded CSV z-score analytics | tested; no device integration |
| AI application development | Python API/CLI/report artifacts | tested; no production server |
| Neural-network programming | optional framework adapters only | no neural model-builder/trainer API |
| Deep learning | optional inference adapters | no DL training/finetuning |
| Machine learning | RandomForest classification/regression | real training/evaluation/prediction tested |
| Generative AI | local text generation adapter | no actual generation test; no image/video synthesis |
| Multimodal AI | optional image input to Ollama | compatible model required; untested inference |
| Image/video/objects/tracking | faces, motion, local detector adapter | motion tested; general detector untested; tracking absent |
| Speech AI | WAV metadata + Whisper adapter | WAV tested; Whisper inference untested; no TTS |
| Agents | DAG planner/specialists/reviewer | tested; no independent multi-LLM deliberation |
| Data science/prediction | CSV profiles and tabular prediction | tested; not universal AutoML |
| Documents | TXT/PDF/DOCX/XLSX extraction | tested; no OCR or legacy DOC/XLS |
| Code engineering | AST/project/risk review | tested; no automatic repair/generated-code execution |
| RAG/search/memory | JSON lexical index + semantic adapter | lexical tested; embeddings untested; no full answer-generation RAG |
| Automation | on-demand local DAG workflows | tested; no persistent scheduler/events |
| Robotics | no control implementation | future; hardware safety/approval required |
| Defensive security | auth-failure log and AST rules | tested; not SIEM/vulnerability scanner |
| Other services | config/exports/plugins/policy | tested as detailed in delivery report |

## Acceptance-based roadmap
- **0.2:** owner license decision, run actual cross-platform CI, per-platform hash
  locks, reproducible Arabic/real-world evaluations, installer/skops integration tests.
- **0.3:** licensed, hashed local text/vision/speech/embedding weights and real CPU/GPU
  inference tests; constrained JSON planning with explicit privilege separation.
- **0.4:** Arabic OCR/layout extraction, temporary-ID multi-object tracking (not face
  identification), licensed TTS, evidence-grounded RAG with abstention evaluation.
- **0.5:** process sandbox/resource limits, cancellation/async, MQTT/ONNX/edge/robot
  adapters with safety tests. No physical actuation without explicit approval.
- **1.0:** stable API contracts, independent security/license review, reproducible
  benchmarks, migrations, incident response and enterprise integration tests.

Additional needs identified: MLOps/experiment tracking, privacy/redaction, fairness
and accessibility, interpretability, group/time-aware evaluation, quantization and
Arabic quality assessment. These are roadmap items, not placeholder functions.
