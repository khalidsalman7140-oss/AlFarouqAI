# AlFarouq AI 0.3.0a1 — الواجهة العربية
مكتبة Python محلية أولاً، نواة خفيفة ومحركات اختيارية. حقوق المؤلف © 2026 خالد
سلمان من اليمن، هندسة حلول الذكاء الاصطناعي، khalidsalman7140@gmail.com.
ابدأ بـ[دليل المستخدم العربي الكامل](USER_GUIDE_AR.md) ثم
[مرجع جميع أكواد الخدمات المنفذة](ALFAROUQ_AI_COMPLETE_CODING_GUIDE.md).
الملكية محفوظة للمؤلف مع ترخيص الكود الحالي Apache-2.0، والصورة والهوية بشروط مستقلة.
هذا إصدار خاص مسلّم ولم ينشر علناً. [تقرير التحقق الحالي](reports/RELEASE_REPORT.ar.md).
دليل المالك خاص ولا يرفع مع المستودع العام. التجهيز لا يساوي النشر ولا إثبات
التشغيل على كل منصة أو كل عتاد. التفاصيل التقنية الإنجليزية التالية مكملة للدليل العربي.

# AlFarouq AI 0.3.0a1
**Local-first Python services, one clear interface.**
Copyright © 2026 Khalid Salman — Yemen — AI Solutions Engineering.
Contact: khalidsalman7140@gmail.com.

```python
from alfarouqai import AI
result = AI("حلل هذا النص", text="الذكاء الاصطناعي يساعد الطلاب.")
print(result.to_dict())
```

## Install this delivered source release
Python 3.10+ targeted; tested Python 3.12/Linux/CPU. Create and activate a venv,
then `python -m pip install .`, or install the matching wheel from dist.
No mandatory runtime dependencies. Add optional engines only when needed, e.g.
`python -m pip install '.[nlp,ml]'`. No automatic download or paid API requirement.
This is a privately delivered alpha, not a claimed public PyPI/GitHub publication.

## Real services and clear limits
64 registered capabilities; the current report separates the 61 exercised example
paths from three actual-weight-unverified adapters. Arabic NLP projects, CSV and
sales forecasts, labeled ML/neural training, pretrained vision, OCR, speech, RAG,
bounded agents, source review, API schema, ONNX/Keras and industrial transports.
Verification counts and platform limits: [current report](reports/RELEASE_REPORT.ar.md).
General natural language routes conservatively; missing labels/references/permissions
are not invented. A small local model is the text fallback, not an unrestricted agent.

## Learn and develop
- [Arabic user guide](USER_GUIDE_AR.md) · [English user guide](USER_GUIDE_EN.md)
- [Every capability with executed snippets](ALFAROUQ_AI_COMPLETE_CODING_GUIDE.md)
- [Offline documentation](docs/index.html) · [API](docs/en/api.md)
- [Release/publishing](PUBLICATION_GUIDE.ar.md) · [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md) · [Licensing](LICENSING.md) · [External notices](THIRD_PARTY_NOTICES.md)

Use Model for a reusable local session or an explicitly approved compatible/Ollama
endpoint. environment/model_plan expose resource hints, not a promise that any huge
model fits. Actual GPU, vendor daemons and cloud platforms were not tested here.
Image/video generation and the legacy image.objects adapter remain actual-weight
unverified. PTY/MQTT/Modbus verification is local software transport, not physical
robot/PLC certification. Not a medical, credit or safety decision system.

## Founder and rights
Khalid Salman / خالد سلمان, Yemen / اليمن. Specialization: Artificial Intelligence;
field: AI Solutions Engineering. Age 22 as originally supplied, not automatically
updated or independently verified. Original portrait: identity/founder/khalid-salman-original.jpg.
Original code/documentation Apache-2.0, copyright remains Khalid Salman. Founder
photo/identity and all third-party code/model/dataset terms are separate. This is
an actual open-source license grant, not a no-copy permission statement. No claim
of ownership over external libraries. The private owner guide is excluded from
public publication staging; review the private ZIP before any public upload.

Prior release documentation/evidence is retained under reports/history and dated
handbooks; the new release report is authoritative for this delivery. No public
repository, PyPI registration or cloud-account authorization was completed here.
