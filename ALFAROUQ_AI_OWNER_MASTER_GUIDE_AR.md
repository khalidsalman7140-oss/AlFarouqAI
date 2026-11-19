# دليل المالك الهندسي والتشغيلي — AlFarouq AI 0.3.0a1
**خاص بخالد سلمان؛ ليس للنشر العام.** © 2026 Khalid Salman — اليمن.
هذا الملف ضمن تسليمك الخاص، وتستبعده أداة publish.py من staging العام. لا يحتوي
مفاتيح حقيقية. لا تجعل كامل ZIP الخاص مستودعاً عاماً قبل مراجعة جميع مكوناته.

## 1. الرؤية والواقع
واجهة موحدة خفيفة مع محركات اختيارية، خدمات جاهزة تحتاجها الدراسة والعمل، ونتائج
وتتبع مصادر قابلين للتصدير. الرؤية واسعة؛ التنفيذ الحالي مجموعة محدودة معلنة من
القدرات لا «كل AI»، ولم تُثبت الأفضلية أو دقة سوقية/سريرية/صناعية. حافظ على
مبدأ: لا adapter يسمى استدلالاً مختبراً إلا بعد تشغيل أوزان وبيانات فعلية.

## 2. مسار التنفيذ والواجهات
AI يمر إلى Client أو model_call حين model صريح؛ Client.plan يختار عبر قواعد محافظة
بالعربية/الإنجليزية، Client.run يتحقق من Capability والحدود وينفذ handler ثم
Result(data/backend/warnings/provenance). النموذج الافتراضي للنصوص صغير ومحلي؛ لا
وكيل غير محدود للأوامر. Model جلسة إعادة استخدام. Config حاوية إعدادات؛
مررها صراحة، ولا تعدّل حقولها بالتوازي بين المهام دون ضبط التزامن ومراجعة core.py.
Registry نقطة إضافة القدرات، وentry-point plugins كود موثوق لا يُحمّل عشوائياً.
مثال خدمة: دالة keyword-only تستقبل config وتعيد Result؛ سجلها في services أو
extensions واكتب اختبارات واضحة. Registry.register وCapability توقيعاتهما أدناه.
كل الملفات الحالية وتعليقات وحدات الكود وتواقيعها موضحة لاحقاً من AST الحقيقي.

## 3. الأمان والموارد والتخزين
افتراضات Config: no network، no remote، no model download. الموافقة لا تعني
صلاحية استخدام البيانات. endpoints في providers/engines تضبط HTTP والهوست؛ راجع
أي توسعة ضد SSRF وredirect وتسريب المفاتيح. لا اعتبار run trusted code كـsandbox.
Atomic writes ترفض overwrite افتراضياً؛ راقب الملفات الحساسة وأذونات SQLite.
VectorStore يخزن النصوص والembeddings في SQLite ويبحث FAISS، وليس تشفيراً أو
إخفاء بيانات. RAG قد يهلوس؛ لا ضمان لصحة citation. لا ترسل document content
إلى remote دون موافقة المستخدم. Model cache يسجل revision والأحجام والهاش؛
إعادة استخدام cache يتحقق من وجود/حجم لا full hash لكل استدعاء؛ راجع checksum
خارجياً قبل الاعتماد على تحميل غير موثوق. لا remote Python code تلقائياً.
resources.environment يقرأ system/cgroup/nvidia-smi إذا وجد. model_plan هامش تقريبي
لا توزيع GPU أو تكميم أو budget KV cache. لم يجر قياس إنتاجي أو اختبار حمل.

## 4. البناء والتحقق وتكرار الإصدار
أنشئ venv مستقل ثم pip install '.[dev]' والإضافات المطلوبة حسب اختباراتك.
نفذ `python -m build` و`python -m twine check dist/*` ثم ثبّت wheel في بيئة نظيفة.
`python scripts/wheel_smoke.py --output ...` من خارج checkout يفحص النواة.
لتحقق النماذج والأجهزة البرمجية جهز ستة caches وTesseract eng/ara وespeak-ng و
Mosquitto، ثم `ALFAROUQ_MODEL_HOME=/your/cache python scripts/run_verification.py --installed`.
Windows env syntax يختلف؛ الاختبار هنا Linux فقط. لا تستعمل .venv ضخماً داخل ZIP.
`python scripts/verify_coding_guide.py --installed` ينفذ نص كل مثال ويقارن task.
`python scripts/build_complete_guide.py` يولد المرجع من نفس النص ونتيجة الاختبار.
`python scripts/build_docs.py` يولد HTML أوفلاين. `python scripts/prepublish_check.py`
فحص heuristic للأسرار والبنية لا ضمان تدقيق أمان؛ لا ترفع .git قديمة أو creds.
`python scripts/package_delivery.py` ينشئ manifest وZIP ثم CRC/هاش؛
`python scripts/validate_project.py --archive /path/to.zip` يفك ويتحقق من كل ملف.
أسماء الإصدارات في pyproject وcore.__version__ يجب أن تتطابق. احتفظ بالمدخل الأصلي
كأرشيف احتياطي منفصل، وليس رجوعاً فوق الكود الحالي. increment PEP440 قبل كل إصدار.

## 5. النشر الحقيقي والمسؤوليات
لم تتوفر مصادقة GitHub/Google/PyPI في جلسة التسليم، ولم ينشر مستودع أو wheel عام.
موافقتك العامة بالنشر عندما تتوفر الصلاحية لا تلغي ضرورة مراجعة هوية المستودع
والترخيص. scripts/publish.py --repo OWNER/REPO dry run؛ --approve-publication فعل
حقيقي و--public يغير الرؤية. لن يكتب فوق remote موجود. لا يطبع token. سجل دخولك
بنفسك gh auth login. PyPI Trusted Publishing يتطلب إنشاء/امتلاك المشروع وإعداد
بيئة GitHub وصلاحيات OIDC؛ اختبر TestPyPI أولاً بعد موافقتك. راجع PUBLICATION_GUIDE.
Hugging Face/Colab/Kaggle قوالب إعداد، وليست منصات مرفوعة أو مصدقة الاختبار.
Google Drive: scripts/upload_to_google_drive.py --help ثم OAuth Desktop credentials
من حسابك ونطاق أقل صلاحية؛ لا تعطي مساعداً كلمة المرور. لا token.json في المصدر.
AI Drive خدمة مختلفة؛ تحقق من رابط المستخدم لا temporary readable URL. لا يمكن
تجاوز شاشة اشتراك مزود ببرمجة محلية. تسليم الهاتف يحتاج ملفاً صغيراً ورابطاً متاحاً.

## 6. الملكية والتراخيص
الطلب الأحدث يطلب النشر مفتوح المصدر، لذلك LICENSE الأصلي الحالي Apache-2.0؛
النسبة وNOTICE لخالد سلمان. لا يجتمع مع حظر مطلق لإعادة الاستخدام؛ إذا أردت
العودة إلى proprietary لنسخة مستقبلية استشر قانونياً وافصل المساهمات والرخص
السارية سابقاً. لا تمحو حقوق المكتبات أو بيانات الأوزان. هوية المؤسس وصورته تحت
identity/founder/LICENSE مستقلة ولا يمنح ترخيص الكود حق انتحال الهوية أو العلامة. راجع
THIRD_PARTY_NOTICES وdocs/research وmodel manifests. أطر MIT/Apache/BSD لا تعني
أن كل dataset/model يسمح تجارياً. أدوات GPL مستقلة مستدعاة عبر subprocess يجب
احترام شروطها عند توزيع binaries؛ هذا التسليم لا يرفقها. النص ليس رأياً قانونياً.

## 7. اكتمال وحدود وخطة تطوير
النواة القديمة والميزات الإضافية مستمرة، والعد النهائي في reports/RELEASE_REPORT.ar.md.
اختبارات حقيقية بأوزان صغيرة وقنوات برمجية لا تثبت دقة كل مجال أو مصنع أو corpus
عربي واسع. توليد الصور/الفيديو وimage.objects القديم adapter-only غير مختبرين
بأوزان في هذا الإصدار. استخدام compatible protocol لا يثبت vLLM/Ollama الأصليين.
لا روبوت أو PLC مادي، لا ASR accuracy benchmark، لا fine-tuning ضخم، لا multimodal
عام، لا dynamic automatic arbitrary-model downloading، ولا اختبار GPU/كل منصات cloud.
المرحلة التالية: golden Arabic dataset، grouped/time split تقييم صيانة، قياس
GPU/context وquantization، streaming/cancellation، اختبارات أحمال API، allowlist
أقوى وremote isolation، تقييم RAG ضد prompt injection، regression للplatforms،
وتثبيت الإصدارات المراجعة حسب مصفوفة كل نظام. لا توسع القائمة أسرع من قابلية
اختبارها. عند خطأ قارن wheel/source/version والبيئة والـcache وسجل backend ثم
أضف failing test قبل الإصلاح. limits ليست sandbox؛ لا تجعل مستخدمين غير موثوقين
يشغّلون الخدمة على خادم ببيانات حساسة بلا عزل حقيقي.

## 8. نماذج الكتالوج الفعلية
```json
{
  "smollm2-135m": {
    "repo": "HuggingFaceTB/SmolLM2-135M-Instruct",
    "license": "Apache-2.0",
    "purpose": "English-first instruction LLM; not a strong Arabic model",
    "extra": "local"
  },
  "minilm-multilingual": {
    "repo": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "license": "Apache-2.0",
    "purpose": "Multilingual sentence embeddings, 384 dimensions",
    "extra": "semantic"
  },
  "whisper-tiny": {
    "repo": "Systran/faster-whisper-tiny",
    "license": "MIT (original Whisper); review conversion notices",
    "purpose": "Multilingual speech recognition, CTranslate2",
    "extra": "speech"
  },
  "mobilenet-v3": {
    "torchvision": "MobileNet_V3_Small_Weights",
    "license": "Review TorchVision weight/dataset terms",
    "purpose": "ImageNet classification",
    "extra": "torchvision"
  },
  "ssdlite320": {
    "torchvision": "SSDLite320_MobileNet_V3_Large_Weights",
    "license": "Review TorchVision weight/COCO data terms",
    "purpose": "COCO object detection",
    "extra": "torchvision"
  },
  "lraspp": {
    "torchvision": "LRASPP_MobileNet_V3_Large_Weights",
    "license": "Review TorchVision weight/COCO/VOC terms",
    "purpose": "21-class semantic image segmentation",
    "extra": "torchvision"
  }
}
```

## 9. التبعيات الاختيارية ومعايير الاختيار
الأطر الناضجة خلف lazy imports: sklearn للـpipelines، TorchVision لأوزان رؤية صغيرة، Transformers للنص، faster-whisper للصوت، FAISS للمقارنة وSQLite للاستمرار؛ اختيارها عملي وليس إثبات الأفضل عالمياً. النواة stdlib. قيود الإصدارات الفعلية:
```toml

ml = ["scikit-learn>=1.5,<2", "pandas>=2.2,<4"]
vision = ["opencv-python-headless>=4.10,<5"]
documents = ["pypdf>=5,<7", "python-docx>=1.1,<2", "openpyxl>=3.1,<4"]
speech = ["faster-whisper>=1.1,<2", "av>=11,<16"]
semantic = ["sentence-transformers>=3,<6"]
objects = ["transformers>=4.45,<6", "torch>=2.5,<3", "Pillow>=10.4,<14", "safetensors>=0.4,<1"]
persistence = ["skops>=0.11,<1"]
local = ["transformers>=4.46,<5", "torch>=2.6,<3", "safetensors>=0.4,<1"]
torchvision = ["torch>=2.6,<3", "torchvision>=0.21,<1", "Pillow>=10.4,<14"]
deep = ["torch>=2.6,<3", "safetensors>=0.4,<1", "scikit-learn>=1.5,<2", "pandas>=2.2,<4"]
vector = ["sentence-transformers>=3.3,<6", "faiss-cpu>=1.8,<2"]
iot = ["pyserial>=3.5,<4", "paho-mqtt>=2,<3"]
diffusion = ["diffusers>=0.31,<1", "transformers>=4.46,<5", "torch>=2.6,<3", "accelerate>=1,<2", "safetensors>=0.4,<1", "imageio-ffmpeg>=0.5,<1"]
nlp = ["nltk>=3.9,<4", "scikit-learn>=1.5,<2"]
api = ["fastapi>=0.115,<1", "uvicorn>=0.30,<1", "httpx>=0.27,<1"]
onnx = ["onnx>=1.17,<2", "onnxruntime>=1.20,<2"]
tensorflow = ["tensorflow-cpu>=2.20,<3"]
industrial = ["pymodbus>=3.11,<4"]
gdrive = ["google-api-python-client>=2,<3", "google-auth-oauthlib>=1,<2"]
dev = ["pytest>=8,<10", "build>=1.2,<2", "twine>=6,<7"]


```

## 10. كل وحدة ووظائفها من المصدر الحقيقي

### `src/alfarouqai/__init__.py`
AlFarouq AI: explicit, lightweight, local-first AI orchestration.


### `src/alfarouqai/__main__.py`
وحدة تهيئة/تصدير؛ راجع التعريفات التالية.


### `src/alfarouqai/agents.py`
Bounded cooperative tool agents: planner, specialists, schema reviewer.

This is a deterministic DAG executor, not an autonomous general intelligence.
References are structured Ref objects, not evaluated strings or generated code.

- Class `Ref`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
- Class `Step`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
- `references(value)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `resolve(value, results)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- Class `AgentTeam`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `plan(self, steps)`
  - `run(self, steps)`

### `src/alfarouqai/api.py`
Optional authenticated text-only FastAPI facade. No API server on import.

- `create_app(*, client=None, token=None)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `schema(*, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/arabic.py`
Arabic-first NLP coursework without hidden corpus or model downloads.

- `normalize(text, *, alef=True, diacritics=True)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `process(*, text, config, stem=True)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- Class `TextModel`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `predict(self, texts)`
- `train_text(*, data, text_column, target, config, seed=42)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `train_report(*, data, text_column, target, config, seed=42)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `topics(*, data, text_column, config, n_topics=3, top_words=8)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `similarity(*, texts, query, config, k=5)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/automation.py`
Persisted local jobs and restricted LLM-guided specialist execution.

- Class `Scheduler`: Caller-driven tick scheduler; no hidden service, thread or remote workflow.
  - `add(self, id, task, inputs, *, run_at)`
  - `tick(self, *, now=None)`
  - `jobs(self)`
  - `cancel(self, id)`
  - `close(self)`
- Class `LLMAgent`: One real local model with planner/specialist/reviewer roles, not separate minds.

The LLM ranks a bounded candidate set; model output can never create code,
file paths or new tool names. Inputs are caller-supplied and immutable by LLM.
  - `run(self, goal, *, inputs_by_task, max_steps=1)`

### `src/alfarouqai/business.py`
Practical business services with explicit units, periods and baseline limits.

- `infer_column(columns, requested, candidates)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `sales_forecast(*, data, config, date_column=None, value_column=None, horizon=1)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `clean(*, data, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `redact(*, text, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `reconcile(*, left, right, key, amount_column, config, tolerance=0.01)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/cli.py`
Small cross-platform command-line interface. JSON inputs are data, never code.

- `main(argv=None)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/client.py`
Unified high-level API with explainable, conservative bilingual routing.

- `default_registry()`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- Class `Client`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `capabilities(self)`
  - `run(self, task, *, verbose=None, **inputs)`
  - `ar(self, text, **kwargs)`
  - `sales(self, data, **kwargs)`
  - `inspect(self, image, reference, **kwargs)`
  - `file(self, document, **kwargs)`
  - `text_train(self, **kwargs)`
  - `train(self, *, data, target, problem, **kwargs)`
  - `deep_train(self, **kwargs)`
  - `prepare(self, task, environment, *, consent=False)`
  - `plan(self, prompt, **inputs)`
- `AI(prompt, *, config=None, model=None, backend='auto', endpoint=None, api_key_env=None, device='auto', **inputs)`: One-call services or explicit model gateway; no hidden installs or hardware promises.

### `src/alfarouqai/core.py`
Public contracts, bounded inputs, explicit configuration and portable exports.

- Class `AlFarouqError`: Actionable base exception; never converted to a fake success.
- Class `ValidationError`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
- Class `MissingDependency`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
- Class `ConsentRequired`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
- Class `UnsupportedTask`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
- `require(module: str, extra: str)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- Class `Config`: Local-only defaults. Model locations must be supplied explicitly.
  - `load(cls, path)`
  - `save(self, path)`
- `atomic_write(path, text: str, *, overwrite=False)`: Exclusive creation by default; existing user files are never silently replaced.
- `input_file(path, config: Config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `fingerprint(path)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `clean_json(value)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- Class `Result`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `to_dict(self)`
  - `export(self, path, *, overwrite=False)`
- Class `Capability`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
- Class `Registry`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `register(self, capability: Capability)`
  - `get(self, name)`
  - `list(self)`
  - `load_plugins(self, *, consent=False)`
- `timed_result(capability, inputs, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/coursework.py`
Classical AI coursework: real shortest-path search, not a robot controller.

- `search(*, grid, start, goal, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/dependencies.py`
Inspect dependencies without importing heavy engines; install only in owned venvs.

- `doctor()`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `installation_plan(extra, environment)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `install_extra(extra, environment, *, consent=False, timeout=600)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/developer.py`
Read-only DB inspection, safe API scaffolding, and untrusted test suggestions.

- `database_profile(*, database, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `tests_generate(*, code, config, model_path=None, max_new_tokens=160)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/documents.py`
Text extraction, lexical retrieval and optional local semantic retrieval.

- `document_read(*, document, config, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- Class `KnowledgeBase`: Bounded lexical TF-IDF/cosine search. Stored documents are data, not commands.
  - `add(self, text, *, source='inline')`
  - `search(self, query, *, k=4)`
  - `save(self, path)`
  - `load(cls, path, *, config=None)`
- Class `SemanticIndex`: Optional CPU embeddings from a reviewed LOCAL SentenceTransformer model.
  - `add(self, text, *, source='inline')`
  - `search(self, query, *, k=4)`

### `src/alfarouqai/engines.py`
Optional local ONNX/Keras inference and explicitly approved HTTP inference.

- `onnx_predict(*, model_path, inputs, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `tensorflow_predict(*, model_path, inputs, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `compatible_chat(*, prompt, endpoint, model, config, api_key_env=None, max_tokens=80)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/extensions.py`
Additive 0.2 registry; original 0.1 handlers are preserved.

- `rag_index(*, document, store, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `rag_search(*, query, store, config, k=4)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `rag_answer(*, question, store, config, model_path=None, k=3, min_score=0.2)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `llm_agent(*, goal, inputs_by_task, config, model_path=None, max_steps=1)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `tick(*, store, config, now=None)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `register_extensions(registry)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/generative.py`
Experimental diffusion adapters. Actual-weight inference NOT verified in 0.2.0.

The release report must not count validation-only tests as image/video inference.
Large local models are user-supplied; no downloads or cloud service are hidden.

- `_validate(model_path, output, extension, consent)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `image_generate(*, prompt, model_path, output, config, steps=20, seed=42, consent=False)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `video_generate(*, prompt, model_path, output, config, frames=17, steps=20, seed=42, consent=False)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/industrial_io.py`
Bounded read-only local Modbus TCP. No discovery, writes or actuation.

- `modbus_read(*, host, address, count, config, port=502, device_id=1)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/industry.py`
Industrial decision-support baselines; never imply equipment safety certification.

- `sensors(*, data, columns, config, sample_rate=None)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `control(*, data, column, baseline, config, sigma=3.0)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `production(*, data, total_column, good_column, config, operating_hours=None)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `maintenance(*, data, target, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `defects(*, image, reference, config, threshold=25, min_area=20, output=None)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/integrations.py`
Explicitly approved MQTT/serial I/O and tests of trusted user projects.

- `_network(host, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `mqtt_publish(*, host, topic, message, config, port=1883, consent=False)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `mqtt_read(*, host, topic, config, port=1883, max_messages=1, duration=3)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `serial_exchange(*, port, config, baudrate=9600, read_bytes=128, command=None, consent=False)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `code_test(*, path, config, consent=False)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/language.py`
Local trained LLM generation, label likelihood and grounded document summaries.

- Class `LocalLanguageModel`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `close(self)`
  - `generate(self, prompt, *, max_new_tokens=96, system='You are a helpful assistant. Be concise and accurate.')`
  - `rank(self, text, candidates)`
- `generate(*, prompt, config, model_path=None, max_new_tokens=96)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `classify(*, text, labels, config, model_path=None)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `code_generate(*, prompt, config, model_path=None, max_new_tokens=160)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `code_repair(*, code, error, config, model_path=None, max_new_tokens=160)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `summarize_document(*, document, config, model_path=None, max_new_tokens=128)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/learning.py`
Actual CPU neural-network training, forecasting, recommendations and anomalies.

- `_network(torch, n_inputs, n_outputs, hidden)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- Class `NeuralModel`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `predict(self, rows)`
  - `save(self, directory)`
  - `load(cls, directory, *, config)`
- `train_neural(*, data, target, problem, config, epochs=80, hidden=(32, 16), seed=42)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `neural_report(*, data, target, problem, config, epochs=80, hidden=(32, 16), seed=42)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `forecast(*, data, column, config, horizon=5)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `recommend(*, data, user, user_column, item_column, rating_column, config, k=5)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `anomalies(*, data, columns, config, contamination=0.1)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/local.py`
Dependency-free text, CSV, source-code, defensive log and sensor analytics.

- `tokens(text)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `text_analyze(*, text, config: Config, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `read_csv(data, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `finite_number(value)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `data_profile(*, data, config, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `sensor_analyze(*, data, column, threshold=3.0, config, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- Class `SourceVisitor`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `add(self, node, rule, message)`
  - `visit_Import(self, node)`
  - `visit_ImportFrom(self, node)`
  - `visit_FunctionDef(self, node)`
  - `visit_ClassDef(self, node)`
  - `visit_Call(self, node)`
  - `visit_ExceptHandler(self, node)`
  - `visit_Assign(self, node)`
- `code_analyze(*, path=None, code=None, config, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `security_logs(*, path, config, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/media.py`
Local media analysis; no silent model downloads or image generation.

- `image_analyze(*, image, config, detect_faces=True, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `video_motion(*, video, config, min_area=300, max_frames=None, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `audio_info(*, audio, config, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `transcribe(*, audio, config, model_path=None, language=None, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `objects_detect(*, image, model_path, config, **kwargs)`: User-provided local Transformers model; remote custom code is always disabled.

### `src/alfarouqai/ml.py`
Leakage-aware tabular training with explicit target and problem type.

- Class `TrainedModel`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `predict(self, rows)`
  - `save(self, path, *, consent=False)`
- `train(*, data, target, problem, config, test_size=0.25, seed=42, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `train_report(*, data, target, problem, config, test_size=0.25, seed=42)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/models.py`
Explicit-consent, revision-recorded model cache. No weights ship in the wheel.

- `cache_root()`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `inventory()`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `_hash(path)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `prepare(name, *, config=None, consent=False)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/providers.py`
Opt-in local Ollama transport. No network calls on import.

- Class `NoRedirect`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `redirect_request(self, req, fp, code, msg, headers, newurl)`
- `ollama_request(config, endpoint, payload)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `chat(*, prompt, config, system=None, image=None, **kwargs)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/resources.py`
Dependency-free resource inspection and explicitly approximate model planning.

- `environment()`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `model_plan(parameters_billion, *, precision_bits=16)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/retrieval.py`
Persistent multilingual embeddings in SQLite; exact cosine search through FAISS.

- Class `VectorStore`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `add(self, text, *, source='inline', chunk_size=700, overlap=100)`
  - `search(self, query, *, k=4)`
  - `answer(self, question, *, model_path=None, k=3, min_score=0.2)`
  - `close(self)`
- `semantic_search(*, text, query, config, store, source='inline')`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/services.py`
Value-oriented service additions; original capability names remain stable.

- `document_insights(*, document, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `document_search(*, document, query, config, k=3)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `group_data(*, data, group_column, config, value_column=None)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `register_services(registry)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `api_schema(*, config)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/shortcut.py`
One-call model gateway; convenience does not create RAM, GPU, or model support.

- Class `Model`: A reusable callable local model or a caller-approved inference endpoint.

Local backend supports reviewed Transformers causal-LM directories and the
curated SmolLM2 model. Arbitrary remote model names are passed to your server,
which must already support/load them and satisfy its own hardware/license needs.
  - `close(self)`
- `model_call(prompt, *, model='smollm2-135m', backend='auto', endpoint=None, config=None, api_key_env=None, max_new_tokens=96, device='auto')`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/speech.py`
Local Whisper recognition and explicit system-executable speech synthesis.

- `recognize(*, audio, config, language=None, model_path=None)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `synthesize(*, text, output, config, voice='en-us', speed=150)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

### `src/alfarouqai/vision.py`
Reviewed official TorchVision weights, OCR and temporary object track IDs.

- Class `VisionEngine`: عقد/حاوية أو واجهة تشغيل حسب الاسم والكود.
  - `image(self, image)`
  - `detect(self, im, threshold=0.4)`
- `detect(*, image, config, threshold=0.4)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `classify(*, image, config, top_k=5)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `segment(*, image, config, output)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- `ocr(*, image, config, language='eng', psm=6)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.
- Class `CentroidTracker`: Temporary IDs only; greedy same-label association, no biometric recognition.
  - `update(self, detections)`
- `track(*, video, config, max_frames=30, threshold=0.4)`: يراجع جسم الدالة في المسار أعلاه؛ استخرج التوقيع مباشرة من المصدر.

## 11. كتالوج جميع الخدمات وتوقيعاتها وأمثلة تنفيذها
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


## 12. شجرة الملفات وتسلسل المسؤوليات
.git أرشيف محلي مستبعد من التسليم، dist نواتج wheel/sdist، src الكود، tests العقود، examples الاستخدام، docs المعرفة، scripts التطوير، deploy قوالب منصات، reports أدلة تحقق تاريخية وحديثة، identity أصل الصورة. لا تحذف historical evidence لكن لا تستعمله كحالة الإصدار الحالي. القائمة التالية ملفات الشجرة وقت التوليد قبل نواتج البناء النهائية؛ DELIVERY_MANIFEST.json هو المرجع النهائي لكل ملف وهاشه.
```text
.github/ISSUE_TEMPLATE/bug_report.md
.github/ISSUE_TEMPLATE/feature_request.md
.github/pull_request_template.md
.github/workflows/ci.yml
.github/workflows/publish.yml
.github/workflows/release-check.yml
.gitignore
.vscode/launch.json
.vscode/settings.json
CHANGELOG.md
CONTRIBUTING.html
CONTRIBUTING.md
DELIVERY_MANIFEST.json
LICENSE
LICENSING.md
MANIFEST.in
NOTICE
PUBLICATION_GUIDE.ar.md
PUBLISH.sh
PUBLISH_WINDOWS.bat
README.ar.html
README.ar.md
README.html
README.md
SECURITY.html
SECURITY.md
START_HERE.md
THIRD_PARTY_NOTICES.html
THIRD_PARTY_NOTICES.md
USER_GUIDE_AR.md
USER_GUIDE_EN.md
archive-validation.json
config.example.json
demo-output/data-report.html
demo-output/text-report.json
deploy/huggingface/Dockerfile
deploy/huggingface/README.md
deploy/huggingface/app.py
dist/alfarouqai-0.2.0a1-py3-none-any.whl
docs/ar/api.html
docs/ar/api.md
docs/ar/architecture.html
docs/ar/architecture.md
docs/ar/capabilities-0.2.html
docs/ar/capabilities-0.2.md
docs/ar/capabilities.html
docs/ar/capabilities.md
docs/ar/curriculum.html
docs/ar/curriculum.md
docs/ar/development.html
docs/ar/development.md
docs/ar/guide.html
docs/ar/guide.md
docs/ar/handbook-0.2.html
docs/ar/handbook-0.2.md
docs/en/api.html
docs/en/api.md
docs/en/architecture.html
docs/en/architecture.md
docs/en/capabilities-0.2.html
docs/en/capabilities-0.2.md
docs/en/capabilities.html
docs/en/capabilities.md
docs/en/curriculum.html
docs/en/curriculum.md
docs/en/development.html
docs/en/development.md
docs/en/guide.html
docs/en/guide.md
docs/en/handbook-0.2.html
docs/en/handbook-0.2.md
docs/index.html
docs/research/SOURCES-0.2.html
docs/research/SOURCES-0.2.md
docs/research/SOURCES.html
docs/research/SOURCES.md
examples/01_quickstart.py
examples/02_machine_learning.py
examples/03_agents.py
examples/04_retrieval.py
examples/05_ollama.py
examples/06_vision.py
examples/07_plugin.py
examples/08_sensors_and_logs.py
examples/09_documents.py
examples/10_local_models.py
examples/11_pretrained_vision.py
examples/12_speech.py
examples/13_neural_network.py
examples/14_semantic_rag.py
examples/15_llm_agents.py
examples/16_scheduler.py
examples/17_analytics.py
examples/18_device_transports.py
examples/data/auth.log
examples/data/knowledge.txt
examples/data/neural.csv
examples/data/ratings.csv
examples/data/sensors.csv
examples/data/students.csv
examples/guide_catalog.py
examples/guide_support.py
identity/founder/LICENSE
identity/founder/README.md
identity/founder/khalid-salman-original.jpg
identity/founder/profile.json
notebooks/AlFarouqAI_0_2_Getting_Started.ipynb
notebooks/README.md
pyproject.toml
reports/FINAL_REPORT.ar.html
reports/FINAL_REPORT.ar.md
reports/FINAL_REPORT.en.html
reports/FINAL_REPORT.en.md
reports/baseline-source-hashes.json
reports/build-0.2.log
reports/build.log
reports/capability-verification-0.2.json
reports/coding-guide-results/agents.llm.json
reports/coding-guide-results/agents.llm.log
reports/coding-guide-results/ai.search.json
reports/coding-guide-results/ai.search.log
reports/coding-guide-results/api.schema.json
reports/coding-guide-results/api.schema.log
reports/coding-guide-results/arabic.process.json
reports/coding-guide-results/arabic.process.log
reports/coding-guide-results/audio.info.json
reports/coding-guide-results/audio.info.log
reports/coding-guide-results/automation.tick.json
reports/coding-guide-results/automation.tick.log
reports/coding-guide-results/code.analyze.json
reports/coding-guide-results/code.analyze.log
reports/coding-guide-results/code.generate.json
reports/coding-guide-results/code.generate.log
reports/coding-guide-results/code.repair.json
reports/coding-guide-results/code.repair.log
reports/coding-guide-results/code.test.json
reports/coding-guide-results/code.test.log
reports/coding-guide-results/code.tests.generate.json
reports/coding-guide-results/code.tests.generate.log
reports/coding-guide-results/data.clean.json
reports/coding-guide-results/data.clean.log
reports/coding-guide-results/data.forecast.json
reports/coding-guide-results/data.forecast.log
reports/coding-guide-results/data.group.json
reports/coding-guide-results/data.group.log
reports/coding-guide-results/data.profile.json
reports/coding-guide-results/data.profile.log
reports/coding-guide-results/data.recommend.json
reports/coding-guide-results/data.recommend.log
reports/coding-guide-results/database.profile.json
reports/coding-guide-results/database.profile.log
reports/coding-guide-results/deep.train.json
reports/coding-guide-results/deep.train.log
reports/coding-guide-results/document.insights.json
reports/coding-guide-results/document.insights.log
reports/coding-guide-results/document.read.json
reports/coding-guide-results/document.read.log
reports/coding-guide-results/document.search.json
reports/coding-guide-results/document.search.log
reports/coding-guide-results/document.summarize.json
reports/coding-guide-results/document.summarize.log
reports/coding-guide-results/finance.reconcile.json
reports/coding-guide-results/finance.reconcile.log
reports/coding-guide-results/image.analyze.json
reports/coding-guide-results/image.analyze.log
reports/coding-guide-results/industry.control.json
reports/coding-guide-results/industry.control.log
reports/coding-guide-results/industry.defects.json
reports/coding-guide-results/industry.defects.log
reports/coding-guide-results/industry.maintenance.json
reports/coding-guide-results/industry.maintenance.log
reports/coding-guide-results/industry.production.json
reports/coding-guide-results/industry.production.log
reports/coding-guide-results/industry.sensors.json
reports/coding-guide-results/industry.sensors.log
reports/coding-guide-results/iot.analyze.json
reports/coding-guide-results/iot.analyze.log
reports/coding-guide-results/iot.modbus.read.json
reports/coding-guide-results/iot.modbus.read.log
reports/coding-guide-results/iot.mqtt.publish.json
reports/coding-guide-results/iot.mqtt.publish.log
reports/coding-guide-results/iot.mqtt.read.json
reports/coding-guide-results/iot.mqtt.read.log
reports/coding-guide-results/llm.chat.json
reports/coding-guide-results/llm.chat.log
reports/coding-guide-results/llm.compatible.json
reports/coding-guide-results/llm.compatible.log
reports/coding-guide-results/local.generate.json
reports/coding-guide-results/local.generate.log
reports/coding-guide-results/ml.train.json
reports/coding-guide-results/ml.train.log
reports/coding-guide-results/nlp.classify.json
reports/coding-guide-results/nlp.classify.log
reports/coding-guide-results/nlp.similarity.json
reports/coding-guide-results/nlp.similarity.log
reports/coding-guide-results/nlp.topics.json
reports/coding-guide-results/nlp.topics.log
reports/coding-guide-results/nlp.train.json
reports/coding-guide-results/nlp.train.log
reports/coding-guide-results/onnx.predict.json
reports/coding-guide-results/onnx.predict.log
reports/coding-guide-results/privacy.redact.json
reports/coding-guide-results/privacy.redact.log
reports/coding-guide-results/rag.answer.json
reports/coding-guide-results/rag.answer.log
reports/coding-guide-results/rag.index.json
reports/coding-guide-results/rag.index.log
reports/coding-guide-results/rag.search.semantic.json
reports/coding-guide-results/rag.search.semantic.log
reports/coding-guide-results/robotics.serial.json
reports/coding-guide-results/robotics.serial.log
reports/coding-guide-results/sales.forecast.json
reports/coding-guide-results/sales.forecast.log
reports/coding-guide-results/security.anomalies.json
reports/coding-guide-results/security.anomalies.log
reports/coding-guide-results/security.logs.json
reports/coding-guide-results/security.logs.log
reports/coding-guide-results/speech.recognize.json
reports/coding-guide-results/speech.recognize.log
reports/coding-guide-results/speech.synthesize.json
reports/coding-guide-results/speech.synthesize.log
reports/coding-guide-results/speech.transcribe.json
reports/coding-guide-results/speech.transcribe.log
reports/coding-guide-results/tensorflow.predict.json
reports/coding-guide-results/tensorflow.predict.log
reports/coding-guide-results/text.analyze.json
reports/coding-guide-results/text.analyze.log
reports/coding-guide-results/video.motion.json
reports/coding-guide-results/video.motion.log
reports/coding-guide-results/video.track.json
reports/coding-guide-results/video.track.log
reports/coding-guide-results/vision.classify.json
reports/coding-guide-results/vision.classify.log
reports/coding-guide-results/vision.detect.json
reports/coding-guide-results/vision.detect.log
reports/coding-guide-results/vision.ocr.json
reports/coding-guide-results/vision.ocr.log
reports/coding-guide-results/vision.segment.json
reports/coding-guide-results/vision.segment.log
reports/coding-guide-verification.json
reports/dependency-check-0.2.log
reports/dependency-check.log
reports/device-example-help.log
reports/document-example.log
reports/environment-0.2.json
reports/environment.json
reports/example-10_local_models.log
reports/example-11_pretrained_vision.log
reports/example-12_speech.log
reports/example-13_neural_network.log
reports/example-14_semantic_rag.log
reports/example-15_llm_agents.log
reports/example-16_scheduler.log
reports/example-17_analytics.log
reports/history/0.2-upload/ALFAROUQAI_FULL_REPORT.txt
reports/history/0.2-upload/LICENSE
reports/history/0.2-upload/NOTICE
reports/history/0.2-upload/README.ar.md
reports/history/0.2-upload/README.md
reports/history/0.2-upload/push.bat
reports/history/0.2-upload/pyproject.toml
reports/installed-source-match.json
reports/installer-success-0.2.json
reports/llm-example-help.log
reports/model-manifests/lraspp.json
reports/model-manifests/minilm-multilingual.json
reports/model-manifests/mobilenet-v3.json
reports/model-manifests/smollm2-135m.json
reports/model-manifests/ssdlite320.json
reports/model-manifests/whisper-tiny.json
reports/notebook-validation.json
reports/package-check-0.2.log
reports/package-check.log
reports/preservation-0.2.json
reports/pytest-0.2.log
reports/pytest-0.2.xml
reports/pytest-0.3.xml
reports/pytest.log
reports/pytest.xml
reports/real-results/agents.json
reports/real-results/classification-report.csv
reports/real-results/classification-report.html
reports/real-results/classification-report.md
reports/real-results/classification-report.txt
reports/real-results/classification.json
reports/real-results/data-profile.json
reports/real-results/defensive-logs.json
reports/real-results/docx-extraction.json
reports/real-results/founder-photo-analysis.json
reports/real-results/lexical-retrieval.json
reports/real-results/motion-fixture.json
reports/real-results/pdf-extraction.json
reports/real-results/predictions.json
reports/real-results/regression.json
reports/real-results/sensors.json
reports/real-results/source-review.json
reports/real-results/text.json
reports/real-results/wav-info.json
reports/real-results/xlsx-extraction.json
reports/regression-0.2.log
reports/releases/0.1.0/FINAL_REPORT.ar.md
reports/releases/0.1.0/FINAL_REPORT.en.md
reports/releases/0.1.0/dist/alfarouqai-0.1.0-py3-none-any.whl
reports/releases/0.1.0/dist/alfarouqai-0.1.0.tar.gz
reports/releases/0.1.0/environment.json
reports/releases/0.1.0/pytest.log
reports/releases/0.1.0/pytest.xml
reports/releases/0.1.0/verification-summary.json
reports/releases/0.1.0/wheel-smoke.json
reports/report-generation.json
reports/third_party_license_evidence/Markdown/licenses/LICENSE.md
reports/third_party_license_evidence/numpy/LICENSE.txt
reports/third_party_license_evidence/opencv-python-headless/LICENSE-3RD-PARTY.txt
reports/third_party_license_evidence/opencv-python-headless/LICENSE.txt
reports/third_party_license_evidence/pandas/licenses/LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/DATEUTIL_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/HAVEN_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/KLIB_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/MUSL_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/NUMPY_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/PACKAGING_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/PSF_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/PYPERCLIP_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/PYUPGRADE_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/SAS7BDAT_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/STATSBASE_JL_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/ULTRAJSON_LICENSE
reports/third_party_license_evidence/pandas/licenses/LICENSES/XSIMD_LICENSE
reports/third_party_license_evidence/pandas/licenses/subprojects/fast_float-8.2.10/LICENSE-APACHE
reports/third_party_license_evidence/pandas/licenses/subprojects/fast_float-8.2.10/LICENSE-BOOST
reports/third_party_license_evidence/pandas/licenses/subprojects/fast_float-8.2.10/LICENSE-MIT
reports/third_party_license_evidence/pypdf/licenses/LICENSE
reports/third_party_license_evidence/python-docx/licenses/LICENSE
reports/third_party_license_evidence/scikit-learn/licenses/COPYING
reports/third_party_license_evidence/scipy/LICENSE.txt
reports/upload-inventory.json
reports/v0.2-learning-results/anomalies.json
reports/v0.2-learning-results/forecast.json
reports/v0.2-learning-results/neural-model/model.json
reports/v0.2-learning-results/neural-model/weights.safetensors
reports/v0.2-learning-results/neural-predictions.csv
reports/v0.2-learning-results/neural-training.json
reports/v0.2-learning-results/recommendations.json
reports/v0.2-model-results/code-generation.json
reports/v0.2-model-results/code-repair.json
reports/v0.2-model-results/crosslingual-semantic-search.json
reports/v0.2-model-results/document-summary.json
reports/v0.2-model-results/image-classification.json
reports/v0.2-model-results/llm-agent.json
reports/v0.2-model-results/local-generation.json
reports/v0.2-model-results/mqtt-publish.json
reports/v0.2-model-results/mqtt-read.json
reports/v0.2-model-results/nlp-classification.json
reports/v0.2-model-results/object-detection.json
reports/v0.2-model-results/ocr-arabic.json
reports/v0.2-model-results/ocr-english.json
reports/v0.2-model-results/rag-answer.json
reports/v0.2-model-results/segmentation.json
reports/v0.2-model-results/semantic-mask.png
reports/v0.2-model-results/serial-pty.json
reports/v0.2-model-results/speech-fixture.wav
reports/v0.2-model-results/speech-recognition.json
reports/v0.2-model-results/speech-synthesis.json
reports/v0.2-model-results/video-tracks.json
reports/verification-run-0.2.json
reports/verification-run-0.3.json
reports/verification-summary.json
reports/verification-workers/worker-0.log
reports/verification-workers/worker-0.xml
reports/verification-workers/worker-1.log
reports/verification-workers/worker-1.xml
reports/verification-workers/worker-2.log
reports/verification-workers/worker-2.xml
reports/verification-workers/worker-3.log
reports/verification-workers/worker-3.xml
reports/verification-workers/worker-4.log
reports/verification-workers/worker-4.xml
reports/verification-workers/worker-5.log
reports/verification-workers/worker-5.xml
reports/verification-workers/worker-6.log
reports/verification-workers/worker-6.xml
reports/verification-workers-0.3/worker-0.log
reports/verification-workers-0.3/worker-0.xml
reports/verification-workers-0.3/worker-1.log
reports/verification-workers-0.3/worker-1.xml
reports/verification-workers-0.3/worker-10.log
reports/verification-workers-0.3/worker-10.xml
reports/verification-workers-0.3/worker-11.log
reports/verification-workers-0.3/worker-11.xml
reports/verification-workers-0.3/worker-12.log
reports/verification-workers-0.3/worker-12.xml
reports/verification-workers-0.3/worker-13.log
reports/verification-workers-0.3/worker-13.xml
reports/verification-workers-0.3/worker-2.log
reports/verification-workers-0.3/worker-2.xml
reports/verification-workers-0.3/worker-3.log
reports/verification-workers-0.3/worker-3.xml
reports/verification-workers-0.3/worker-4.log
reports/verification-workers-0.3/worker-4.xml
reports/verification-workers-0.3/worker-5.log
reports/verification-workers-0.3/worker-5.xml
reports/verification-workers-0.3/worker-6.log
reports/verification-workers-0.3/worker-6.xml
reports/verification-workers-0.3/worker-7.log
reports/verification-workers-0.3/worker-7.xml
reports/verification-workers-0.3/worker-8.log
reports/verification-workers-0.3/worker-8.xml
reports/verification-workers-0.3/worker-9.log
reports/verification-workers-0.3/worker-9.xml
reports/verified-requirements-0.2.txt
reports/verified-requirements.txt
reports/vision-example.log
reports/wheel-smoke.json
scripts/build_complete_guide.py
scripts/build_docs.py
scripts/capture_examples.py
scripts/capture_upgrade.py
scripts/package_delivery.py
scripts/prepublish_check.py
scripts/publish.py
scripts/run_verification.py
scripts/upload_to_google_drive.py
scripts/validate_project.py
scripts/verify_coding_guide.py
scripts/wheel_smoke.py
src/alfarouqai/__init__.py
src/alfarouqai/__main__.py
src/alfarouqai/agents.py
src/alfarouqai/api.py
src/alfarouqai/arabic.py
src/alfarouqai/automation.py
src/alfarouqai/business.py
src/alfarouqai/cli.py
src/alfarouqai/client.py
src/alfarouqai/core.py
src/alfarouqai/coursework.py
src/alfarouqai/dependencies.py
src/alfarouqai/developer.py
src/alfarouqai/documents.py
src/alfarouqai/engines.py
src/alfarouqai/extensions.py
src/alfarouqai/generative.py
src/alfarouqai/industrial_io.py
src/alfarouqai/industry.py
src/alfarouqai/integrations.py
src/alfarouqai/language.py
src/alfarouqai/learning.py
src/alfarouqai/local.py
src/alfarouqai/media.py
src/alfarouqai/ml.py
src/alfarouqai/models.py
src/alfarouqai/providers.py
src/alfarouqai/py.typed
src/alfarouqai/resources.py
src/alfarouqai/retrieval.py
src/alfarouqai/services.py
src/alfarouqai/shortcut.py
src/alfarouqai/speech.py
src/alfarouqai/vision.py
tests/test_additional_verification.py
tests/test_core.py
tests/test_engines_03.py
tests/test_models.py
tests/test_optional.py
tests/test_resources_03.py
tests/test_services_03.py
tests/test_shortcuts_03.py
tests/test_system.py
tests/test_transport.py
tests/test_upgrade.py
```
