# Practical learning curriculum
[Handbook](handbook-0.2.md) · [العربية](../ar/curriculum.md)

Learn the foundations, run the example, inspect real outputs, then report limitations.
The facade reduces boilerplate, not the need for mathematics/data/license literacy.

| Unit | Experiment | API/example |
|---|---|---|
| 1 Python environments | venv and VS Code interpreter | 01 |
| 2 Data literacy | CSV/missing values/reports | data.profile |
| 3 Basic NLP | frequency/extractive summary | text.analyze |
| 4 Local LLM | actual weights and hallucination review | 10 |
| 5 Label scoring | likelihood vs calibrated confidence | nlp.classify |
| 6 Basic vision | faces vs identity | 06 |
| 7 Detection/classification | COCO vs ImageNet categories | 11 |
| 8 Segmentation | numeric masks and class semantics | vision.segment |
| 9 OCR | printed Arabic/English and scan quality | vision.ocr |
| 10 Video | motion vs temporary tracks/occlusion | video.track |
| 11 Speech | synthesize, transcribe, record errors | 12 |
| 12 ML | leakage, splits, preprocessing, metrics | 02 |
| 13 Deep learning | multilayer network, loss and epochs | 13 |
| 14 Model persistence | safetensors/JSON and restored predictions | 13 |
| 15 Time/recommendation | chronological validation and cold start | forecast/recommend |
| 16 Documents | extraction vs full comprehension | 09 |
| 17 RAG/embeddings | cross-language retrieval, citations and faithfulness | 14 |
| 18 Agents/automation | deterministic DAG vs LLM plan, scopes and ticks | 03/15/16 |
| 19 Devices/security | approved transports, anomalies vs attacks | 17/18 |
| 20 Research engineering | reproducibility, licenses, evaluation and reporting | tests/reports |

Capstone: licensed teaching documents -> extraction -> index -> retrieve ->
evidence-returning answer -> human error analysis. Do not treat generated text
as a source of truth. CNN/Transformer finetuning, SLAM and diffusion video need
additional lessons/hardware; they are not silently counted as completed APIs.
