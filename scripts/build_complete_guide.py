"""Generate the requested single coding reference from actually executed snippets."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from examples.guide_catalog import CASES,COMMON,UNVERIFIED
from alfarouqai import Client

INTRO='''# ALFAROUQ AI COMPLETE CODING GUIDE
## الدليل العملي الشامل — 0.3.0a1
تاريخ التحقق: 2026-11-19. الكود الحالي Apache-2.0؛ حقوق المؤلف لخالد سلمان من اليمن.

### ما المكتبة وما حدودها؟
بوابة Python محلية أولاً لأدوات AI وتحليل البيانات وخدمات عملية. تعيد نتائج
حقيقية مع backend وتحذيرات ومصدر، ولا تخلق عتاداً أو دقة أو صلاحية قانونية.
كل مثال خدمة قابل للتشغيل أدناه نُفذ من النص نفسه، وسجله ومخرجاته في
reports/coding-guide-results. ثلاثة موصلات غير مختبرة مفصولة بلا مثال نجاح وهمي.

## التثبيت والإعداد
من المجلد المفكوك أنشئ بيئة: `python -m venv .venv` ثم فعلها بالطريقة المناسبة
لنظامك: `.venv\\Scripts\\Activate.ps1` في PowerShell أو `source .venv/bin/activate`
في Linux/macOS. ثبّت من المصدر `python -m pip install .` أو wheel المرفق في dist.
لا تفترض أن الاسم العام على PyPI محجوز للمشروع قبل التحقق من النشر الفعلي.

النواة بلا اعتماديات تشغيل إلزامية. أضف فقط ما تحتاجه، مثل
`python -m pip install '.[nlp,ml]'`. الإضافات الفعلية: ml، vision، documents،
speech، semantic، objects، persistence، local، torchvision، deep، vector، iot،
diffusion، nlp، api، onnx، tensorflow، industrial، gdrive، dev. المحركات الثقيلة
اختيارية؛ قد تحتاج برامج نظام مستقلة مثل Tesseract وحزم eng/ara وespeak-ng وMosquitto.
PyTorch CPU wheels تقلل تنزيل CUDA غير المطلوبة؛ اتبع إرشادات نظامك الرسمية.
Python 3.10+ مستهدف، والتنفيذ المحلي هنا Python 3.12/Linux/CPU. لا تدّعي مصفوفة CI
أن Windows/macOS أو Colab/Kaggle/Hugging Face قد اختبرت فعلياً في هذه المهمة.

### الشبكة والأوزان والمفاتيح
لا تنزيل أو تثبيت خفي عند import. config.allow_network وallow_model_download
موافقتان صريحتان. models تحت ~/.cache/alfarouqai/models أو ALFAROUQ_MODEL_HOME.
راجع الرخصة والحجم والمراجعة المثبتة قبل الموافقة. لا أوزان ضخمة داخل ZIP.
api_key_env يستقبل اسم متغير البيئة لا قيمة المفتاح. لا تضع الأسرار في المصدر
أو notebook؛ استعمل مدير أسرار بيئتك. Remote endpoints تحتاج allow_remote وHTTPS.
سكربت Google Drive يحتاج OAuth منك؛ لم يُربط حساب Google أثناء التسليم.

## بوابة سطر واحد وموديل كبير حسب الموارد
اختبر المثال التالي بأوزان حقيقية مخزنة محلياً:
```python
from alfarouqai import AI
result = AI('What is the capital of France?', model='smollm2-135m', max_new_tokens=24)
```
كما اختبر AI على prompt عام بلا model؛ هذا افتراض محلي للتوليد النصي، لا إذن
بتنفيذ أوامر النظام أو تحكم صناعي. التحليل ذو الملفات أو الهدف الواضح يختار
الخدمة المدعومة؛ الغموض أو نقص target/reference لا يملآن بالتخمين.

Model جلسة قابلة للاستعمال المتكرر مع close/with. backend local يقبل النموذج
المختار أو مجلد causal-LM محلياً متوافقاً مع Transformers، لا كل معمارية.
backend ollama أو compatible يمرر اسم النموذج إلى خادمك، وهو الذي يتحمل العتاد.
Model/AI model gateway يدعمان device=auto/cpu/cuda؛ اختبر CPU ورفض CUDA غير المتاح،
ولم يختبر استدلال GPU فعلي. environment وmodel_plan أدوات تقدير لا ضمان fit.
تقدير weights لا يحسب KV cache والسياق والدفعات والتكميم كاملاً. لا وعد بتشغيل
أكبر نموذج على الهاتف؛ اقرأ الدليل فيه وشغّل الحساب على عتاد مناسب أو endpoint.

## التهيئة المشتركة للأمثلة
نفّذ التالي مرة من جذر AlFarouqAI المفكوك ثم كتلة الخدمة. أدوات fixtures من
المصدر المرفق وتولد بيانات تعليمية مصطنعة؛ ليست قراءات مصنع أو مرضى حقيقية.
لا يتم تشغيل خادم عند الاستيراد. الملفات المؤقتة تمنع استبدال بياناتك.
```python
'''
ENDSETUP='''
```
كل مثال كامل محفوظ أيضاً تحت examples/guide، ويمكن تشغيله من Terminal من جذر
المشروع. في Jupyter/Colab/Kaggle ثبّت wheel ثم ارفع المصدر لأدوات الأمثلة واضبط
current directory إلى جذر المشروع، ثم شغّل التهيئة والكتلة نفسها. هذا تعليم
تشغيل، لا ادعاء أن المنصات السحابية نفذت في التحقق المحلي. لملفاتك الخاصة
استبدل DATA/PHOTO بالمسارات التي تملك حق معالجتها؛ الخدمة نفسها غالباً سطر واحد.

## جميع الخدمات الفعلية
'''
ENDING='''
## النتائج والتصدير والأخطاء
Result.to_dict يعرض البيانات والمحرك والتحذيرات. export يدعم JSON/CSV/MD/HTML/TXT؛
هذه الصيغ اختبرت. CSV يصدّر rows إن وجدت وإلا مفاتيح/قيماً؛ HTML يهرب النصوص.
الكتابة ترفض الملف القائم إلا overwrite=True. أعد تهيئة OUT عند تكرار مثال
ينشئ ملفاً جديداً. زمن المثال يتضمن التحميل ولا يصلح وحده لمقارنة أداء النماذج.
Config(verbose=True) يعرض start/done/backend/error type في stderr دون طباعة
المفاتيح أو المحتوى الخاص. لا ادعاء نسبة تقدم داخل كل نموذج خارجي.

MissingDependency: ثبت extra في المفسر الذي تستعمله. ConsentRequired: لم تمنح
صلاحية الشبكة/التنزيل/الأجهزة/تشغيل الكود. ValidationError: مدخل ناقص أو غير صالح.
أخطاء المحرك الأصلية قد تنتقل كذلك. Config.timeout يحد HTTP وبعض أدوات النظام،
وليس sandbox عاماً أو حداً مضموناً لكل CPU/RAM. code.test يختبر كوداً موثوقاً فقط؛
-I والمهلة لا تمنعان وصوله إلى الملفات والشبكة. لا تنفذ اقتراح LLM تلقائياً.

## مشاريع تجمع الخدمات
- طالب NLP: arabic.process للاحتفاظ بالنص المنظف، nlp.train للتصنيف المسمي، ثم
TextModel.predict. إزالة التكرار لا تمنع تسرب المؤلف/الموضوع/الزمن؛ قيّم تقسيماً
مناسباً. ISRI اشتقاق تقريبي لا lemmatizer سياقي، وTF-IDF لفظي لا دلالي.
- مصنع: اجمع industry.sensors ثم industry.control على baseline مستقلة، وفحص
industry.defects بصورة مرجعية مصطفة، ثم industry.production. لا تساوِ control
limits مع specification limits، ولا تدّعِ OEE دون مدخلاته. الصيانة مصنف labels
تاريخي لا عمر متبقٍ أو shutdown آلياً؛ يلزم تقييم مجمّع حسب الآلة والزمن.
- شركة: sales.forecast يجمع شهوراً مكتملة بصيغة ISO ويتحقق زمنياً. ليس وعد مبيعات
ولا سببياً. finance.reconcile Decimal لمطابقة الدفاتر لا موافقة تحويل مالي أو
كشف احتيال مثبت. database.profile يقرأ المخطط والعد دون تعديل قاعدة البيانات.
- مستشفى: data.group لبيانات مواعيد مجهولة الهوية وزمن الانتظار؛ privacy.redact
يخفي بريد/هاتف تقريبياً وليس امتثال HIPAA/GDPR أو تعمية كاملة. لا تشخيص أو علاج.
- مستندات: document.read -> rag.index -> rag.search.semantic -> rag.answer. المصادر
والإزاحات متاحة، لكن entailment وصحة الاستشهاد غير مضمونين. PDF مصور يحتاج OCR
غير موصول تلقائياً بكل الصفحات. لا تعتبر جواب النموذج مرجع حقيقة.
- وكلاء: AgentTeam حتمي وLLMAgent يختار من قائمة آمنة؛ الأدوار تشترك في نموذج
لا عقول مستقلة. Scheduler ينفذ عند tick ولا يعمل وجهازك مغلق. MQTT ACK ليس
إثبات فعل جهاز. Serial/Modbus اختبرا بوسيط/خادم محلي وPTY، لا PLC/روبوت مادي.

## سياق أمثلة الاتصالات
model_server يشغّل LLM حقيقياً عبر بروتوكول مرجعي؛ لا يعني تثبيت vLLM/Ollama.
broker يحتاج Mosquitto محلياً؛ modbus_server خادم محلي للاختبار. مثال PTY خاص
بـLinux/POSIX، وعلى Windows تحتاج منفذ COM حقيقياً وبروتوكولاً مصرحاً. لا مسح
شبكات أو إرسال أوامر أجهزة دون موافقة. API النصية محكومة بمفتاح وقائمة صغيرة؛
لا يغني هذا عن TLS وحدود موارد ومراقبة وتدقيق أمان إنتاجي.

## إضافة قدرة وتطوير مشروعك
Capability اسم + handler keyword + required + extra؛ أعد Result، واستورد المحرك
عند الطلب واحترم الموافقات والحدود. اختبر النجاح والفشل والرخصة والموارد، ثم
حدّث tests وguide_catalog وشغّل verify_coding_guide قبل إضافة مثال «مختبر».
حافظ على أسماء الخدمات القديمة وعقود schema_version. راجع دليل المالك لملفات
المشروع والبناء والإصدار. الدليل الحالي لا يعرض دقة مضمونة أو أفضلية عالمية.

## النشر والتنزيل
راجع PUBLICATION_GUIDE.ar.md. زرا النشر يطلبان أدوات وحساباً مخولاً وتأكيداً؛
Trusted Publishing يحتاج إعداد مالك PyPI/GitHub مرة واحدة. لا رفع عام تم هنا.
Google Drive يحتاج Desktop OAuth من صاحب الحساب؛ التخطيط اختبر دون ربط حسابك.
AI Drive مختلف. لا رابط أو سكربت يلغي سياسة الاشتراك؛ نسخة المشروع صغيرة،
والأوزان اختيارية من مصادرها. الرخصة الحالية Apache-2.0 مع نسبة العمل لخالد
سلمان؛ الصورة والهوية والأطر والأوزان تحت شروطها المستقلة.
'''

def preview(x):
    if isinstance(x,dict):return {k:preview(v) for k,v in list(x.items())[:5]}
    if isinstance(x,list):return [preview(v) for v in x[:2]]
    if isinstance(x,str) and len(x)>180:return x[:180]+' …'
    return x

def main():
    v=json.loads((ROOT/'reports/coding-guide-verification.json').read_text());checked={x['task']:x for x in v['examples']}
    assert set(checked)==set(CASES) and all(x['passed'] for x in checked.values())
    caps=Client().capabilities();assert set(CASES)|set(UNVERIFIED)=={c['name'] for c in caps}
    parts=[INTRO,COMMON,ENDSETUP]
    for i,c in enumerate(caps,1):
        name=c['name'];parts.append(f'### {i}. `{name}`\n\n{c["description"]}\n\n**المتطلبات:** `{c["extra"] or "core/system"}`. **المدخلات:** `{", ".join(c["required"]) or "راجع الوظيفة"}`.\n\n')
        if name in UNVERIFIED:parts.append('**غير مثبت باستدلال فعلي:** '+UNVERIFIED[name]+'\n\n');continue
        body=CASES[name];parts.append('**نص نُفّذ بنجاح** بعد التهيئة المشتركة:\n\n```python\n'+body+'\nprint(result.to_dict())\n```\n\n')
        result=json.loads((ROOT/'reports/coding-guide-results'/(name+'.json')).read_text())
        parts.append('**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**\n\n```json\n'+json.dumps({'backend':result['backend'],'data':preview(result['data']),'warnings':result.get('warnings',[])[:2]},ensure_ascii=False,indent=2)+'\n```\n\n')
        p=ROOT/'examples/guide'/(name.replace('.','_')+'.py');p.parent.mkdir(exist_ok=True)
        p.write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\n'+COMMON+'\n'+body+'\nprint(result.to_dict())\n')
        parts.append('**Terminal:** `python examples/guide/'+p.name+'` من جذر المشروع.\n\n')
    parts.append(ENDING);p=ROOT/'ALFAROUQ_AI_COMPLETE_CODING_GUIDE.md';p.write_text(''.join(parts),encoding='utf-8');print('Complete guide:',len(caps),'services;',len(CASES),'executed examples;',p.stat().st_size,'bytes')
if __name__=='__main__':main()
