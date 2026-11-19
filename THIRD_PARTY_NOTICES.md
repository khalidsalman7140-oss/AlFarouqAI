# 0.2 third-party addendum
Original AlFarouq AI code stays PROPRIETARY. No MIT/Apache/GPL public grant applies to original code.
External projects alone retain their respective licenses. No weights or external executables are bundled.

| Added external engine | License boundary |
|---|---|
| PyTorch / TorchVision | BSD-style libraries and separate weight/training-data conditions; inspect exact release notices |
| FAISS | MIT, Meta copyright; external library only |
| Transformers / SentenceTransformers | Apache-2.0 framework; model-specific terms remain separate |
| SmolLM2-135M-Instruct | Model card Apache-2.0; English-first limitations |
| multilingual MiniLM-L12-v2 | Model card Apache-2.0; exact revision recorded |
| Whisper tiny conversion / CTranslate2 | Original/model/converter notices independently reviewed; manifests record source, not blanket clearance |
| Tesseract | Apache-2.0 external executable and language data |
| espeak-ng | GPL-3.0-or-later external executable, invoked as a separate program, NOT linked/vendored or applying GPL to our original code; review combined-distribution legal implications |
| Eclipse Paho MQTT | Dual EPL-2.0 / EDL-1.0, inspect deployed distribution |
| pySerial | BSD-style, inspect installed metadata/license |
| Diffusers / CogVideoX / Stable Diffusion | Library/model terms separate; no model deployed or weights bundled; actual inference not verified |

See docs/research/SOURCES-0.2.md and reports/model-manifests. This is not a full legal audit or commercial-use warranty.

# Third-party notices and license boundaries
AlFarouq AI original works: copyright Khalid Salman; see LICENSE.
Third-party projects retain their own copyrights/licenses. No third-party sources,
model weights, datasets or binaries are bundled in the core wheel. Full checkout
includes only original teaching fixtures, tests, founder asset and generated reports.
Installing optional dependencies fetches distributions that carry their own notices.

| Component | Initial license classification | Usage and verification |
|---|---|---|
| Python | PSF | interpreter, not bundled |
| scikit-learn | BSD-3-Clause | optional; actual training/prediction tested |
| pandas / NumPy / SciPy | BSD family; inspect binary-vendor notices too | optional tabular/transitive stack; versions in environment report |
| OpenCV >=4.10,<5 | Apache-2.0 library | optional faces/motion tested; native/codec/data-file notices may differ |
| pypdf | BSD-3-Clause | optional; actual installed package metadata/licenses recorded |
| python-docx | MIT | optional; installed package metadata/licenses recorded |
| openpyxl | MIT | optional; installed package metadata/licenses recorded |
| faster-whisper | MIT, preliminary source listing | optional adapter, not installed or inference tested here |
| SentenceTransformers | Apache-2.0 library | optional adapter, no deployed model license clearance |
| Transformers | Apache-2.0 library | optional adapter, no deployed weights |
| PyTorch | BSD-style library, plus notices | optional detector backend, not inference tested |
| safetensors | Apache-2.0 library | optional detector weights format |
| skops | BSD-3-Clause | optional save-only adapter, not persistence-tested |
| pytest / build / twine / setuptools / wheel | inspect exact metadata and included notices | build/test tools, not core runtime |
| Markdown (documentation renderer) | BSD-3-Clause per installed metadata | documentation build only; not core runtime |

Evidence: [research sources](docs/research/SOURCES.md), and the mechanically recorded
installed distribution metadata in reports/environment.json. The latter may include
transitive/development tools; it is NOT a verified complete SBOM or legal audit.
Binary distributions can carry additional licensed components. Full available
license/NOTICE files for the executed runtime engines are copied to
reports/third_party_license_evidence/ as evidence, without claiming those works.

No external model weights were downloaded, bundled or trained. Commercial rights
for a specific future model are UNVERIFIED until its exact revision/license,
training-data restrictions, acceptable-use rules, attribution and redistribution
conditions are reviewed. Do not equate "free download" with unrestricted use.

Ultralytics/YOLO is NOT a dependency. The vendor offers AGPL/enterprise options;
compatibility with this project's restrictive original-work license needs separate
review. ONNX Runtime, MQTT, robotics middleware and OCR are roadmap options only.
This is an engineering inventory, not legal advice or a warranty of license fitness.

جميع الحقوق للمكونات الخارجية محفوظة لأصحابها. لا ينقل شرط ملكية خالد سلمان
حقوق أي عمل خارجي إليه، ولا يمنح استخداماً تجارياً لكل نموذج بصورة تلقائية.
