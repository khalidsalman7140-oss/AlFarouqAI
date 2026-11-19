# كتاب الاستخدام والتعلم — AlFarouq AI 0.2.0 Alpha
[الرئيسية](../../README.ar.md) · [الدليل السابق المحفوظ](guide.md) · [English](../en/handbook-0.2.md)

## 1. ماذا تغير، وما الذي لا ندّعيه
هذا تطوير إضافي للإصدار 0.1.0، وليس مشروعاً جديداً. بقيت واجهاته واختباراته
الأصلية. أضيفت محركات ونماذج مدربة محلية، وتدريب عصبي، وقاعدة متجهات، ووكلاء
مدعومة بنموذج، وتكاملات أجهزة محكومة بالموافقة. لا يوجد دليل أن المكتبة أفضل
من كل مكتبة أخرى؛ الأدق أنها تختصر استعمال أدوات متخصصة وتوضح مصدر نتائجها.
لا يمكن لواجهة موحدة أن تلغي قيود العتاد والترخيص وجودة البيانات.

## 2. تثبيت خفيف ثم إضافة ما تحتاجه
أنشئ بيئة افتراضية وفعلها كما في الدليل الأصلي، ثم من المجلد المفكوك:
```bash
python -m pip install .
# اختر الإضافات المطلوبة فقط، لا تثبت الجميع:
python -m pip install '.[local]'
python -m pip install '.[torchvision,vision]'
python -m pip install '.[speech]'
python -m pip install '.[vector]'
python -m pip install '.[deep,iot]'
```
لأجهزة CPU يمكن تثبيت إصدار PyTorch المناسب من فهرس CPU الرسمي أولاً، بدلاً من
تنزيل حزم CUDA غير المطلوبة. اتبع إرشادات PyTorch الخاصة بنظامك، ولا تفترض أن
عجلات Linux التي اختبرت هنا مناسبة لكل جهاز. راجع reports/verified-requirements-0.2.txt
لإصدارات بيئة التحقق؛ هذا جرد اختبار، وليس lock محمولاً مضموناً لكل منصة.

`Client.prepare('vision.detect', '.alfarouq-env')` يعرض خطة الاعتماديات. إضافة
`consent=True` تنفذها داخل بيئة مخصصة وفق حواجز الإصدار السابق. بعدها ثبّت
المكتبة داخل تلك البيئة واختر مفسرها؛ لا تستطيع العملية الحالية استيراد بيئة
أخرى آلياً. لا يثبّت import أو الاستدعاء المعتاد شيئاً خفياً.
Tesseract وحزم لغاته وespeak-ng ووسيط MQTT برامج نظام اختيارية مستقلة لا يحاول
pip تثبيتها. اختبر الآن مسار تثبيت إضافة iot الشبكي في بيئة مخصصة، ثم استوردت الحزم بمفسرها دون تعديل البيئة الحالية.

## 3. النماذج: تنزيل مرة بموافقة ثم عمل محلي
```python
from alfarouqai import Client, Config
ai = Client(Config(allow_network=True, allow_model_download=True))
```
هذان الخياران موافقة صريحة على تنزيل النماذج المعروفة عند أول احتياج. بعدها
يمكن استعمال `Client()` دون شبكة إذا بقيت الأوزان في cache. المسار الافتراضي
`~/.cache/alfarouqai/models`، ويغيره المتغير المعلن `ALFAROUQ_MODEL_HOME`.
`model_inventory()` يعرض الأسماء، و`prepare_model(name, ..., consent=True)`
يهيئ نموذجاً بعينه. لكل تنزيل سجل مراجعة مصدر وإصدار immutable وبصمات SHA-256.
فحص الوجود أثناء الاستعمال ليس تدقيق سلامة تشفيرياً دائماً ولا توقيع ناشر.

| الاسم | الوظيفة | ما شُغّل |
|---|---|---|
| smollm2-135m | نصوص وكود وتخطيط محدود | SmolLM2-135M-Instruct؛ إنجليزي أساساً |
| minilm-multilingual | تضمين وبحث متعدد اللغات | MiniLM-L12-v2؛ بحث عربي/إنجليزي فعلي |
| whisper-tiny | تعرف الكلام | CTranslate2 CPU/int8؛ عينة إنجليزية مولدة صوتياً |
| mobilenet-v3 | تصنيف صور | MobileNet V3 Small / ImageNet |
| ssdlite320 | كشف أشياء | SSDlite / COCO |
| lraspp | تقسيم دلالي | LRASPP / أصناف VOC |

الأوزان ليست داخل ZIP عمداً: حجمها المجمع نحو 847 ميجابايت في التحقق. إبقاء
الحزمة صغيرة يقلل صعوبات التنزيل؛ مصادر النماذج مستقلة ولا تتطلب اشتراك API
مدفوعاً. لا تُعد رخصة إطار العمل ترخيصاً لكل وزن أو بيانات تدريبه؛ راجع السجل
وبطاقة النموذج قبل الاستخدام التجاري أو إعادة التوزيع.

## 4. سطر أو سطران للاستخدام بعد الإعداد
```python
r = ai.run('vision.detect', image='photo.jpg')
r.export('objects.json')
```
ويمكن الاختصار:
```python
from alfarouqai import AI
r = AI('vision.classify', image='photo.jpg')
```
الاستدعاء بالاسم متعمد لأنه لا يخمن نوع المهمة. الأوصاف العربية/الإنجليزية
القديمة ما زالت تعمل ضمن حدود الموجه القديم. للكتابة الحرة مع اختيار محرك صريح:
```python
r = ai('Explain gravity briefly.', task='local.generate')
```
البساطة تخص الاستدعاء بعد تثبيت الإضافة والموافقة على النموذج؛ لا نخفي متطلبات
العتاد أو تثبيت النظام أو موافقات الأجهزة داخل سطر سحري.

## 5. النصوص وNLP وتوليد المحتوى والكود
```python
ai.run('local.generate', prompt='Explain a neural network in two sentences.')
ai.run('nlp.classify', text='This book is wonderful.', labels=['positive','negative'])
```
التصنيف يرتب تسمياتك باستخدام احتمالية النموذج، وليس نموذج مشاعر متخصصاً،
ودرجة relative_score غير معايرة. المولد الافتراضي 135M صغير، وليس إثبات جودة
عربية متقدمة. يمكنك تمرير model_path محلياً لنموذج Transformers متوافق ومدقق؛
قد تحتاج ذاكرة أكبر. لا كود remote موثوق تلقائياً، ولا تحميل pickle لغوي.
المدخل يقتطع عند 1024 token، والإخراج مقيد؛ لا يصلح كملخص شامل لكتاب طويل.

```python
ai.run('code.generate', prompt='Write a Python function add(a,b).')
ai.run('code.repair', code='def add(a,b)\n return a+b', error='missing colon')
```
هذه اقتراحات حقيقية يولدها النموذج، وليست دليلاً على صحة البرنامج. الملفات
الأصلية لا تعدل تلقائياً. لتحليلها دون تشغيل: `code.analyze`. لتشغيل اختبارات
unittest لمشروع موثوق فقط:
```python
ai.run('code.test', path='trusted_tests', consent=True)
```
العملية الفرعية والمهلة ليستا sandbox أمنياً؛ الاختبارات تملك صلاحيات المستخدم.
لا تشغّل كوداً مجهولاً أو مولداً تلقائياً في جهاز يحمل أسراراً.

## 6. الرؤية والـOCR والفيديو
```python
ai.run('vision.detect', image='photo.jpg', threshold=0.4)
ai.run('vision.classify', image='photo.jpg', top_k=5)
ai.run('vision.segment', image='photo.jpg', output='mask.png')
ai.run('vision.ocr', image='scan.png', language='ara+eng')
ai.run('video.track', video='clip.mp4', max_frames=30)
```
الكشف أصناف COCO، والتصنيف أصناف ImageNet؛ ليسا تعريف هوية. mask.png صورة
قيمها الرقمية معرّفات أصناف، وليست صورة فوتوغرافية محسنة أو تقسيم instances.
الفيديو يجمع كشفاً مدرباً مع ربط مراكز مؤقت؛ قد تتبدل المعرفات عند التداخل.
لا تحليل أفعال أو مشاعر أو هوية أشخاص. OCR يحتاج tesseract وحزمة ara للعربية؛
اختبر على نص مطبوع مصطنع واضح، لا ضمان للخط اليدوي أو الصور الرديئة.

## 7. الكلام: من صوت إلى نص ومن نص إلى صوت
```python
ai.run('speech.synthesize', text='Hello world.', output='speech.wav', voice='en-us')
ai.run('speech.recognize', audio='speech.wav', language='en')
```
الأول نطق تقليدي فعلي عبر espeak-ng وليس استنساخ صوت عصبي؛ الثاني Whisper
مدرب فعلي. في التحقق أخطأ التفريغ في بداية العينة، رغم التقاطه بقية كلماتها.
نجاح تشغيل النموذج لا يساوي دقة 100%. اختبارات العربية الصوتية والتقييم البشري
ما زالت مطلوبة. عولج تعارض PyAV 19 مع faster-whisper بتقييد av>=11,<16.

## 8. تعلم آلة وشبكات عصبية
التدريب الجدولي القديم scikit-learn محفوظ. أضيف PyTorch MLP بطبقتين مخفيتين:
```python
model = ai.deep_train(data='numeric.csv', target='label', problem='classification')
model.predict([{'x':1.0, 'y':2.0}]).export('prediction.json')
```
الأعمدة هنا مثال لملفك؛ كلها عددية دون نقص. تصنيف أو انحدار صريح، وتقسيم قبل
تعلم التحجيم، وتقييم held-out. البيانات التعليمية لا تثبت تعميماً بحثياً.
`model.save('new-model-directory')` يحفظ safetensors وJSON دون pickle، والاستعادة
عبر `NeuralModel.load(directory, config=Config())`. ليس تدريب CNN/Transformer
عاماً ولا fine-tuning للنموذج اللغوي. التحكم بهندسة النموذج يتم عبر hidden وepochs.

## 9. بيانات وتنبؤ وتوصيات وأمن دفاعي
```python
ai.run('data.forecast', data='series.csv', column='temperature', horizon=5)
ai.run('data.recommend', data='ratings.csv', user='u1', user_column='user', item_column='item', rating_column='rating')
ai.run('security.anomalies', data='metrics.csv', columns=['bytes','connections'])
```
التنبؤ خط اتجاه خطي مع تحقق زمني 80/20، لا ARIMA أو موسمية أو سببية.
التوصية user-cosine collaborative filtering صغيرة البيانات، لا حل cold start.
IsolationForest يكشف شذوذاً لا يثبت هجوماً. التحليل الدفاعي القديم للسجلات
والكود محفوظ، ولا توجد أدوات استغلال أو مسح شبكات تلقائي.

## 10. المستندات وRAG والذاكرة المتجهية
```python
ai.run('rag.index', document='notes.pdf', store='knowledge.sqlite')
ai.run('rag.answer', question='What measures temperature?', store='knowledge.sqlite')
```
البديل القابل للتحكم:
```python
from alfarouqai import VectorStore
with VectorStore('knowledge.sqlite') as db:
    db.add('المستشعر يقيس درجة الحرارة.', source='lesson')
    hits = db.search('measuring temperature')
```
تضمين متعدد اللغات مدرب، FAISS IndexFlatIP فعلي، وتخزين دائم SQLite مع مصادر
وإزاحات. يعاد بناء الفهرس من المتجهات، فلا تحميل كائنات pickle. السقف 10000
مقطع، وليس قاعدة موزعة للمليارات. هوية الأوزان ثابتة عبر نقل مسار cache.
RAG يعيد المصادر ويستطيع الامتناع عند نقص الاسترجاع، لكن صدق الإجابة وصحة
الاقتباس غير مضمونين؛ لم تنفذ آلية إثبات entailment. `document.summarize` يقرأ
جزءاً محدوداً ثم يلخصه؛ لا يدّعي فهم كل صفحات كتاب. OCR لا يعمل تلقائياً على
PDF مصور بعد. KnowledgeBase وSemanticIndex القديمان لم يحذفا.

## 11. الوكلاء والأتمتة
```python
from alfarouqai import LLMAgent
r = LLMAgent(client=ai).run('Analyze this text', inputs_by_task={'text.analyze':{'text':'Hello world.'}})
```
مخطط لغوي يرتب خيارات محددة باحتمالية النموذج، ينفذ أداة من قائمة آمنة، ثم
مراجع لغوي. الأدوار تشترك في النموذج، وليست عقولاً مستقلة متفوقة. لا يسمح
بتوليد اسم أداة جديد أو مسار أو أمر shell؛ المدخلات من المستخدم فقط. أقصى أربع
خطوات، ويمكن أن يمتنع. AgentTeam القديم مناسب لخطط DAG الحتمية والأوضح للأبحاث.

```python
from alfarouqai import Scheduler
s = Scheduler('jobs.sqlite'); s.add('job1','text.analyze',{'text':'Hello'},run_at=0)
s.tick()  # لا يعمل شيء في الخلفية دون تشغيل tick
```
SQLite يحتفظ بالحالة؛ المهام مطالَبة مرة واحدة، لا exactly-once بعد انهيار نظام.
لا daemon خفي ولا ادعاء جدولة دائمة أثناء إغلاق Python. الشبكة والأجهزة محظورة
في قائمة هذا المجدول. أغلقه عبر s.close().

## 12. IoT والروبوتات: ما اختبر وما لم يختبر
```python
ai.run('iot.mqtt.read', host='127.0.0.1', topic='sensors/temperature')
ai.run('robotics.serial', port='/dev/ttyUSB0', command='STATUS\n', read_bytes=128, consent=True)
```
تحتاج موافقة الشبكة لـMQTT، وallow_remote مع TLS للخادم البعيد. النشر يمكن
أن يشغّل محركات ولذلك يتطلب consent=True، ولا يتاح للوكلاء الافتراضيين.
اختبر وسيط Mosquitto حقيقي محلياً، وقراءة/كتابة Serial على pseudo-terminal
حقيقي في نواة Linux. لا يوجد حساس أو روبوت مادي في البيئة؛ لا نثبت الحركة أو
الأسلاك أو السلامة أو kinematics/SLAM. لا ترسل أوامر عتاد قبل مراجعة بروتوكوله.

## 13. التوليد الصوري والمرئي: تجريبي غير مؤكد التشغيل
`image.generate` موصل StableDiffusionPipeline، و`video.generate` موصل CogVideoX.
كُتب مسارهما وتحققت حواجز المدخلات والموافقة فقط؛ **لم يُشغّلا بأوزان فعلية**.
يلزمان model_path محلياً مدققاً وconsent=True وموارد أكبر بكثير. لا أوزان عشوائية
تحت اسم اختبار نجاح، ولا نعد النتيجة الفيديوية مكتملة. لم يثبت توافق كل نسخ
Diffusers أو المعماريات أو الأداء. لا تعتمد عليهما إنتاجياً قبل اختبارات عتادك.

## 14. الاختبارات والتصدير والعمل في بيئات مختلفة
شغّل `python -m pytest` لاختبارات الانحدار؛ الاختبارات ذات الأوزان لا تعمل إلا
`ALFAROUQ_RUN_MODELS=1` وبعد تهيئة cache. النجاح الكامل المحلي وتفاصيله في
reports/pytest-0.2.xml والتقرير النهائي، لا تخلط ذلك بتشغيل GitHub Actions أو
Colab/Kaggle: لم تشغل تلك المنصات خلال التسليم. Notebook وتعليمات رفع wheel
في notebooks/، وقالب Hugging Face في deploy/. لا روابط مستودع وهمية ولا نشر تلقائي.

كل قدرة تعيد Result قابل التصدير بالصيغ الخمس السابقة. الملفات الناتجة الفعلية
في reports/v0.2-model-results تشمل الصوت والـmask وتقارير النماذج، ومعها بصمات
الأوزان ومصادرها في reports/model-manifests. لا تنقل ملفات SQLite مفتوحة أثناء
الكتابة دون إغلاقها أو أخذ نسخة احتياطية متسقة.

## 15. الملكية، الانتشار، والأبحاث
جميع الأعمال الأصلية والهوية حقوق خاصة لخالد سلمان من اليمن، ولا إذن للجمهور
بالنسخ أو التعديل أو الاقتباس أو الاشتقاق أو إعادة التوزيع دون موافقة كتابية.
الأطر والأوزان الخارجية تحت تراخيصها وحدها. لا نشر خارجي قبل موافقة المالك.
هذا الاختيار يمنع تبني المشروع كمكتبة عامة حرة الاستخدام تلقائياً؛ لا يمكن
الجمع بين منع الاستخدام العام وادعاء سهولة تبنٍّ مفتوح بلا إذن. يمكن للمالك
إصدار أذونات خاصة أو عقود تعليمية مكتوبة دون تغيير ملكيته؛ لا أصدرها نيابة عنه.

لزيادة القيمة: وثّق زمن التهيئة منفصلاً عن الاستدلال، انشر اختبارات قابلة
للإعادة بعد الموافقة، قارن جودة مهام حقيقية، وفر أمثلة عربية ودفاتر دراسية،
وأعلن حدود كل نموذج. لا يعد اسم المكتبة أو عدد المحركات وحدهما سبباً للتفوق.
استشهد بالنموذج الأصلي، نسخته وبصمته، البيانات، البذرة، البيئة، وحدود التقييم
في بحثك. لا تعتبر درجات عينات الاختبار الصغيرة نتائج مقارنة علمية.
