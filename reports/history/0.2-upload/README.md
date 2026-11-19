# Current release: 0.2.0 Alpha — incremental, not publicly published
[Updated handbook](docs/en/handbook-0.2.md) · [Curriculum](docs/en/curriculum.md) · [Current coverage](docs/en/capabilities-0.2.md) · [Current report](reports/FINAL_REPORT.en.md)

The core remains lightweight and Khalid Salman's original rights are reserved.
The preserved 0.1.0 content below describes its historical status; see 0.2 docs above.

---

# AlFarouq AI
**0.1.0 — local alpha delivery, not published to GitHub or PyPI.**

[العربية](README.ar.md) · [Guide](docs/en/guide.md) · [Offline project page](docs/index.html) · [Capabilities](docs/en/capabilities.md) · [Delivery report](reports/FINAL_REPORT.en.md)

A lightweight, local-first Python entry point for students, researchers, developers,
and organizations. One public API, explicit capabilities, optional engines,
bounded agent workflows, and exportable results with backend provenance.
The core has **zero mandatory runtime dependencies**. This is not a universal model
and does not claim to implement every AI research area.

## Install from this checkout
```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install .
python examples/01_quickstart.py
```
Do not assume `pip install alfarouqai` from the public index points to this project:
name availability/ownership has NOT been checked. Install this folder or its wheel.

```python
from alfarouqai import AI, Client
result = AI('analyze this text', text='AI helps students. Local tools help researchers.')
print(result.data)
result.export('report.json')
print(Client().capabilities())
```
For real tabular training: `python -m pip install '.[ml]'`, then
`python examples/02_machine_learning.py`. The data are synthetic teaching data,
not evidence of generalization on real-world tasks.

## Founder and original-work rights
<img src="identity/founder/khalid-salman-original.jpg" alt="Khalid Salman, founder-supplied photo" width="180">

**خالد سلمان — Khalid Salman** · **Yemen** · **22 years old as supplied**.
Specialization: **Artificial Intelligence**. Field: **AI Solutions Engineering**.
Project: **AlFarouq AI**. Email: [khalidsalman7140@gmail.com](mailto:khalidsalman7140@gmail.com).
Biography supplied by the founder, not independently verified or automatically
age-updated. The original photo is unmodified and is not model-training data.

All original code, designs, components and identity of AlFarouq AI are owned by
Khalid Salman, the project founder. Copying, quoting, reusing or redistributing
original project works requires prior written permission from the owner.
Third-party libraries/tools retain their own rights and licenses; no ownership of
external work is claimed. See [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md).

**Licensing conflict resolved conservatively:** the requested no-reuse restriction
is incompatible with the OSI open-source definition. This delivery reserves rights;
it is NOT OSI open source and grants no general public reuse permission. A future
MIT/Apache-2.0 or other open license requires the owner's decision. Brand/photo rights
can be managed separately. This is not legal advice.

## Honest implementation boundary
Tested local tools: text statistics/extractive summary, CSV, AST/project review,
defensive logs, recorded sensors, tabular training/evaluation/prediction, image
statistics/face detection, video motion, document extraction, lexical retrieval,
result exports and bounded DAG workflows. Local LLM/vision-chat, speech transcription,
semantic embeddings and general object-detection **adapters are implemented but have
not run model-weight inference in this delivery**. No weights are bundled.
Not implemented: image/video synthesis, TTS, neural-network training API, finetuning,
robot control, connected IoT, persistent person tracking, autonomous code execution,
or independent multi-LLM deliberation.

Read the [guide](docs/en/guide.md), [architecture](docs/en/architecture.md),
[development guide](docs/en/development.md) and [security policy](SECURITY.md).
