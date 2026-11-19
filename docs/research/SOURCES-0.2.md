# 0.2 research evidence | مصادر التطوير

Date: 2026-11-15. Retrieved pages informed incremental decisions, not a blanket legal/security audit.

- [SmolLM2 model card](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) — Apache-2.0 model card; 135M is English-first and limited; actual local inference ran.
- [TorchVision detector](https://docs.pytorch.org/vision/main/models/generated/torchvision.models.detection.ssdlite320_mobilenet_v3_large.html) — COCO pretrained SSDlite, about 13.4MB weights; actual inference ran.
- [TorchVision segmentation](https://docs.pytorch.org/vision/main/models/generated/torchvision.models.segmentation.lraspp_mobilenet_v3_large.html) — 21 VOC labels, about 12.5MB; actual class mask exported.
- [Multilingual MiniLM](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) — 384-dimensional embeddings; cross-language retrieval actually ran.
- [Whisper conversion](https://huggingface.co/Systran/faster-whisper-tiny) — Local CTranslate2 weights; actual CPU/int8 recognition, errors retained.
- [Tesseract CLI](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html) — TSV OCR with word boxes/confidence; Arabic/English fixture ran.
- [FAISS](https://github.com/facebookresearch/faiss) — MIT external engine; cosine via normalized inner products, actual IndexFlatIP search.
- [espeak-ng](https://github.com/espeak-ng/espeak-ng) — GPL-3.0-or-later separate executable; real WAV synthesis, not neural voice cloning.
- [Paho MQTT](https://github.com/eclipse-paho/paho.mqtt.python) — Callback API v2 and QoS1 broker acknowledgement; actual Mosquitto test.
- [Paho license](https://github.com/eclipse-paho/paho.mqtt.python/blob/master/LICENSE.txt) — Dual EPL/EDL source retrieved in search; inspect exact deployed terms.
- [pySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) — Actual local serial transport; kernel PTY test, no physical device claim.
- [PyTorch serialization](https://docs.pytorch.org/docs/stable/notes/serialization.html) — weights_only is defense in depth, not permission to load untrusted models.
- [CogVideoX](https://huggingface.co/docs/diffusers/en/api/pipelines/cogvideox) — GPU-oriented high-memory examples; no inference success claimed under this environment.

Original code remains proprietary; external licenses apply ONLY to external works. No model weights/system executables bundled. Model manifests record exact revisions and SHA256 values.
