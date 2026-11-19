> هذا المحتوى محفوظ من 0.1.0. الحالة الحالية في [كتاب 0.2](handbook-0.2.md) و[مصفوفة 0.2](capabilities-0.2.md).

# دليل الاستخدام العربي
[الرئيسية](../../README.ar.md) · [القدرات](capabilities.md) · [English](../en/guide.md)

## 1. ماذا تثبّت ولماذا
تحتاج النواة Python 3.10 أو أحدث، وقد جرى الاختبار المحلي على Python 3.12/Linux
فقط. توافق الأنظمة والإصدارات الأخرى مستهدف بقالب CI، وليس اختباراً منفذاً هنا.
أنشئ بيئة افتراضية، فعّلها، ثم ثبّت من مجلد المشروع: `python -m pip install .`.
للتطوير استخدم `python -m pip install -e '.[dev]'`. يمكن تثبيت ملف wheel من dist
بدلاً من المجلد. البناء قد يحتاج اتصالاً لتنزيل setuptools، رغم خلو النواة من
اعتماديات التشغيل. لا تتضمن الحزمة نماذج ولا أدوات خارجية مركبة مسبقاً.

| الحاجة | التثبيت من جذر المشروع | المحرك |
|---|---|---|
| بيانات وتنبؤ جدولي | `python -m pip install '.[ml]'` | scikit-learn + pandas |
| وجوه وحركة | `python -m pip install '.[vision]'` | OpenCV 4.x |
| PDF/Word/Excel | `python -m pip install '.[documents]'` | pypdf / python-docx / openpyxl |
| تفريغ صوتي | `python -m pip install '.[speech]'` | faster-whisper، أوزان منفصلة |
| بحث دلالي | `python -m pip install '.[semantic]'` | SentenceTransformers، أوزان منفصلة |
| كشف أشياء عام | `python -m pip install '.[objects]'` | Transformers + PyTorch، أوزان منفصلة |
| حفظ نموذج | `python -m pip install '.[persistence]'` | skops؛ حفظ فقط في هذا الإصدار |

الميزانية النقدية صفر من ناحية عدم إلزام خدمة مدفوعة؛ العتاد والكهرباء والإنترنت
والتخزين ليست مجانية بالضرورة. لا توجد ذاكرة RAM واحدة تناسب كل النماذج.
ابدأ بالنواة والبيانات الصغيرة، ثم راجع بطاقة النموذج وحجمه وموارد جهازك.
لا تختَر أكبر نموذج لمجرد أنه أكبر؛ قوته تقاس بجودة مهمتك وقيود الجهاز والترخيص.

## 2. ثلاثة مستويات للتحكم
```python
from alfarouqai import AI, Client
# مبتدئ: وصف قصير ضمن مهام الموجه المدعومة
r = AI('حلل هذا النص', text='Python مفيدة. الذكاء الاصطناعي يساعد الطلاب.')
print(r.data['keywords'])
# مطور: قدرة صريحة لا تعتمد على فهم الطلب
client = Client()
r = client.run('data.profile', data='examples/data/students.csv')
# باحث: خطة تراجعها قبل تشغيل أي محرك
print(client.plan('أنشئ نموذج للتنبؤ', data='examples/data/students.csv'))
```
`AI` دالة تعيد Result، و`Client` يحتفظ بالإعدادات والسجل بين الاستدعاءات.
الموجّه حتمي ثنائي اللغة ومحدود، لا يدّعي فهم كل وصف طبيعي. إذا كانت المهمة
ملتبسة يطلب استدعاءً صريحاً، وإذا نقص الهدف أو نوع التدريب يتوقف برسالة واضحة.
لا يثبّت شيئاً ولا ينزل نموذجاً نتيجة استدعاء AI.

## 3. تدريب وتنبؤ حقيقيان
```python
from alfarouqai import Client
model = Client().train(
    data='your-training.csv',
    target='label',
    problem='classification',  # أو regression
    seed=42,
)
print(model.report.data['metrics'])
# يجب أن تطابق الأعمدة جميع الميزات، دون target
pred = model.predict([{'feature1': 1.5, 'feature2': 'category'}])
pred.export('predictions.csv')
```
المثال أعلاه قالب لملفك، وليس ملف البيانات المرفق. المثال القابل للتشغيل مباشرة:
`python examples/02_machine_learning.py`. يفصل التدريب والاختبار قبل تعلم
التعويض والترميز والتحجيم، ويحذف عمود الهدف، ويقبل فئات جديدة عند التنبؤ.
الميزات العددية تُستنتج من التدريب فقط. يدعم بيانات جدولية عددية وفئوية، لا صوراً
ولا نصوصاً خاماً كتدريب NLP. يرفض أقل من 12 صفاً والتسميات الناقصة.
يلزم تصنيف بفئتين على الأقل وصفين لكل فئة وإمكان تكوين تقسيم طبقي صالح.
النتائج: Accuracy وF1 للتصنيف، MAE وR² للانحدار. التقسيم عشوائي 75/25 افتراضياً
ولا يناسب السلاسل الزمنية أو المرضى المتكررين أو البيانات المجمعة دون تعديل.
افحص تسرب المعلومات: لا تستخدم أعمدة مشتقة من النتيجة أو مكررات عبر التقسيم.
النتيجة المرتفعة على البيانات التعليمية المصطنعة ليست دليلاً على تعميم حقيقي.

`Client.run('ml.train', ...)` يعيد تقريراً فقط؛ `Client.train(...)` يعيد النموذج
القابل للتنبؤ. `model.save('model.skops', consent=True)` يحتاج إضافة persistence،
ولم يُختبر حفظه هنا؛ لا توجد واجهة تحميل نموذج في هذا الإصدار. لا نستخدم pickle.

## 4. الصور والفيديو والصوت
```python
client.run('image.analyze', image='photo.jpg')
client.run('video.motion', video='clip.avi', max_frames=100, min_area=300)
client.run('audio.info', audio='recording.wav')
```
الصور: أبعاد ومتوسط ألوان وكشف وجوه أمامية تقليدي، لا تعرف هوية.
الفيديو: فرق إطارات ومناطق حركة محدودة بميزانية، لا أسماء أشياء ولا تتبع هوية
ولا فهم سلوك. يتوقف بعد 300 إطار افتراضياً ويصرّح بالاقتطاع. ترميزات الفيديو
مرهونة ببناء OpenCV في جهازك. audio.info يقبل PCM WAV فقط ولا يفرغ الكلام.

```python
client.run('image.objects', image='photo.jpg', model_path='/local/reviewed/detector')
client.run('speech.transcribe', audio='speech.wav', model_path='/local/whisper-ct2', language='ar')
```
هذان موصلان برمجيان لم يختبرا استدلالاً فعلياً هنا. لا أوزان مرفقة.
يتطلب الكشف نموذج Transformers محلياً متوافقاً مع object-detection وبصيغة
safetensors؛ `trust_remote_code=False` دائماً. لا يتم تنزيله تلقائياً.
يتطلب الصوت نموذج Whisper محولاً إلى CTranslate2؛ التنفيذ CPU/int8، والتنزيل
ممنوع ما لم تمنح allow_model_download صراحة. راجع ترخيص كل وزن وبياناته أولاً.

## 5. المستندات والاسترجاع
```python
from alfarouqai import Client, KnowledgeBase
client = Client()
doc = client.run('document.read', document='examples/data/knowledge.txt')
kb = KnowledgeBase(chunk_size=800, overlap=100)
kb.add(doc.data['text'], source='knowledge.txt')
hits = kb.search('خالد سلمان', k=3)
print(hits.data['rows'])
kb.save('knowledge.json')
restored = KnowledgeBase.load('knowledge.json')
```
استرجاع TF-IDF/تشابه جيب تمام بالكلمات، يدعم حروف العربية ولا يفهم المرادفات
دلالياً. النتائج تحمل المصدر وبداية ونهاية المقطع، ولا تختلق إجابات.
للبحث الدلالي: `SemanticIndex('/local/reviewed/embedding-model')` ثم add/search.
الموصل الدلالي يتطلب أوزاناً محلية ولم يختبر استدلالاً هنا. RAG التوليدي الكامل
يحتاج تأليف سياق موثّق ثم نموذجاً محلياً؛ لم يُضمّن ادعاء بدقة الإجابة.
PDF المصور يحتاج OCR غير موجود بعد. DOCX جداول وفقرات، XLSX قيم مخزنة لا
إعادة حساب صيغ. لا تحافظ عملية الاستخراج على كل تنسيق المستند.

## 6. الأكواد والمشاريع والأمن والمستشعرات
```python
client.run('code.analyze', path='src/alfarouqai')
client.run('code.analyze', code='import os\nos.system(command)\n')
client.run('security.logs', path='examples/data/auth.log')
client.run('iot.analyze', data='examples/data/sensors.csv', column='temperature', threshold=3)
```
AST يحلل الاستيرادات والدوال والفئات وبعض المخاطر النمطية دون تشغيل الكود.
لا يصحح الكود تلقائياً ولا يختبر مشروعاً مجهولاً، ولا يغني عن مراجعة أمنية.
سجلات الأمن: فشل مصادقة فقط، لا ماسح شبكات ولا كشف تهديد شامل.
IoT: قيم مسجلة في CSV وz-score، لا اتصال MQTT ولا حساس فعلي ولا محركات.
توجد حدود للملفات والصفوف؛ للملفات العدائية استخدم عزلاً مستقلاً على مستوى النظام.

## 7. الوكلاء: تنفيذ حقيقي محدود وواضح
```python
from alfarouqai import AgentTeam, Step, Ref
team = AgentTeam(workers=2)
r = team.run([
    Step('read', 'document.read', {'document':'examples/data/knowledge.txt'}, agent='reader'),
    Step('summarize', 'text.analyze', {'text':Ref('read','text')}, agent='summarizer'),
])
print(r.data['trace'])
```
المخطط يتحقق من DAG والميزانية وقائمة الأدوات، ثم يشغل التخصصات، ويُمرر نتائج
حقيقية بالمراجع، ويراجع بنية النتيجة. لا يحلل Ref ككود. تُنفذ المستويات المستقلة
بالتوازي عند workers>1، وتفشل المهام عند الخطأ دون نجاح وهمي أو إعادة غير منضبطة.
المراجع لا يثبت صحة النتائج دلالياً؛ هذا ليس نقاشاً بين نماذج لغوية مستقلة.
LLM محظور في قائمة الفريق الافتراضية. فتح أداة صراحة لا يلغي سياسة الشبكة.

## 8. النموذج اللغوي المحلي وVS Code
```python
from alfarouqai import Client, Config
client = Client(Config(model='YOUR_LOCAL_MODEL', allow_network=True))
r = client.run('llm.chat', prompt='اشرح التعلم الآلي')
print(r.data['text'])
```
ثبت Ollama خارج المشروع، راجع ترخيص نموذجك ونزّله بإرادتك، وشغله محلياً أولاً.
المكتبة لا تسحبه ولا توفر اشتراكاً. الشبكة ممنوعة افتراضياً حتى loopback.
للخادم البعيد يلزم allow_remote=True وHTTPS أيضاً. لا ترسل بيانات خاصة لخادم
غير موثوق. قد يوجه خادم محلي إلى نموذج سحابي باسم مستعار؛ راجع إعدادات Ollama.
موصل الصور في llm.chat يحتاج نموذجاً بصرياً متوافقاً ولا يثبت أن كل LLM بصري.

في VS Code افتح مجلد AlFarouqAI، وثبّت إضافة Python الرسمية، واختر مفسر .venv
من Python: Select Interpreter، ثم شغّل المثال أو ملف الإعداد في .vscode.
المكتبة تعمل مع Python العادي وJupyter؛ لا توجد إضافة VS Code خاصة بالمشروع.

## 9. الإعدادات والتصدير والأخطاء
```python
from alfarouqai import Config, Client, AlFarouqError
config = Config(max_input_bytes=5_000_000, max_video_frames=100)
config.save('my-config.json')  # يرفض استبدال ملف قائم
try:
    result = Client(Config.load('my-config.json')).run('text.analyze', text='مرحبا')
    result.export('report.html')
except AlFarouqError as error:
    print(type(error).__name__, str(error))
```
JSON/CSV/MD/HTML/TXT مدعومة. التصدير ينشئ ملفاً جديداً ولا يستبدل إلا overwrite=True.
CSV يصدر data.rows إذا توفرت، وإلا مفاتيح/قيم؛ يقي قيم الصيغ قدر الإمكان.
HTML يهرب النصوص. أخطاء نقص الاعتماديات أو الموارد أو الموافقة صريحة.
Config.timeout خاص بطلب HTTP، وليس مهلة عامة توقف محركات CPU أو الوكلاء.

## 10. مدير الاعتماديات
`alfarouq doctor` يفحص وجود الحزم، لا يثبت توافق جميع الإصدارات.
`alfarouq install-extra vision --environment .alfarouq-env` يعرض الخطة فقط.
إضافة `--yes` تمنح موافقة لتنزيل حزم PyPI في بيئة مخصصة جديدة/مُدارة، لا بيئة
المستخدم الحالية. يلزم بعدها تثبيت المكتبة في تلك البيئة واختيار مفسرها، كما
تشرح الرسالة الناتجة. لا يصبح الكود الحالي قادراً على استيراد حزم بيئة أخرى
بطريقة سحرية. الاعتماديات والأوزان عمليتان منفصلتان. مسار النجاح الشبكي للمثبت
لم يُختبر آلياً هنا؛ اختبرت حواجز الموافقة ومنع البيئات غير المُدارة.
