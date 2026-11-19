"""Write current-release evidence and internal reading copy without publishing."""
from pathlib import Path
import hashlib,json,sys,xml.etree.ElementTree as ET,importlib.metadata,zipfile,tarfile,html
ROOT=Path(__file__).resolve().parents[1]

def main():
    from alfarouqai import Client,__version__
    tests=json.loads((ROOT/'reports/verification-run-0.3.json').read_text())
    assert tests['installed_wheel'] and tests['counts']=={'tests':133,'failures':0,'errors':0,'skipped':0},tests
    guide=json.loads((ROOT/'reports/coding-guide-verification.json').read_text())
    assert guide['installed_wheel'] and len(guide['examples'])==61 and all(x['passed'] for x in guide['examples'])
    # Worker zero is re-run after final documentation adjustments; refresh aggregate.
    aggregate=ET.Element('testsuites');counts={'tests':0,'failures':0,'errors':0,'skipped':0}
    for worker in tests['workers']:
        p=ROOT/worker['log'];xml=p.with_suffix('.xml')
        for suite in ET.parse(xml).getroot().iter('testsuite'):
            aggregate.append(suite)
            for k in counts:counts[k]+=int(suite.get(k,0))
    assert counts==tests['counts']
    for k,v in counts.items():aggregate.set(k,str(v))
    ET.ElementTree(aggregate).write(ROOT/'reports/pytest-0.3.xml',encoding='utf-8',xml_declaration=True)
    smoke=json.loads((ROOT/'reports/wheel-smoke-0.3.json').read_text());assert smoke['passed'] and smoke['wheel_version']==__version__
    dist=importlib.metadata.distribution('alfarouqai');matches={}
    for p in (ROOT/'src/alfarouqai').glob('*.py'):
        installed=Path(dist.locate_file('alfarouqai/'+p.name));matches[p.name]=hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(installed.read_bytes()).digest()
    assert all(matches.values())
    core=ET.parse(ROOT/'reports/core-only-0.3.xml').getroot();coretests=sum(int(s.get('tests',0)) for s in core.iter('testsuite'))
    assert coretests==88
    with zipfile.ZipFile(ROOT/'dist/alfarouqai-0.3.0a1-py3-none-any.whl') as z:assert z.testzip() is None
    with tarfile.open(ROOT/'dist/alfarouqai-0.3.0a1.tar.gz') as t:assert not any(Path(n).name.startswith('ALFAROUQ_AI_OWNER_MASTER_GUIDE_AR') for n in t.getnames())
    receipt={'version':__version__,'date_utc':'2026-11-19','capabilities':len(Client().capabilities()),'installed_wheel_tests':tests,'core_only_tests':88,'exact_installed_examples':61,'source_wheel_match':matches,'private_owner_guide_excluded_from_public_staging_and_sdist':True,'untested_adapters':guide['untested'],'github_authenticated':False,'google_drive_authenticated':False,'public_publication_performed':False,'weights_bundled':False}
    (ROOT/'reports/release-verification-0.3.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
    ar='''# تقرير تسليم AlFarouq AI — 0.3.0a1
تاريخ: 2026-11-19. حقوق المؤلف © 2026 خالد سلمان — اليمن.

## الخلاصة التنفيذية
تطوير تراكمي للملف المرفق، وليس مشروعاً جديداً. حافظت النسخة على أسماء الخدمات
والواجهات والاختبارات القديمة، وأضيفت خدمات عملية وتوثيق كامل وبوابة Model وفحص
موارد. ZIP خاص لا ينشر نفسه. أوصاف الرؤية ليست وعوداً بأن كل مهمة أو أكبر نموذج
يعمل على أي عتاد أو بأن جودة النموذج الصغير تصلح للإنتاج.

## أدلة التحقق الحالية
| الفحص | النتيجة المقاسة |
|---|---|
| إصدار metadata والكود | 0.3.0a1 |
| القدرات المسجلة | 64 |
| كامل الاختبارات ضد wheel المثبت | 133 ناجحاً، 0 فشل، 0 أخطاء، 0 تخطٍ |
| اختبار النواة في بيئة منفصلة بلا محركات اختيارية | 88 ناجحاً، 45 مستبعداً بقصد حسب العلامات |
| أمثلة الدليل المنفذة من النص نفسه ضد wheel | 61 ناجحاً |
| المتطلبات الإلزامية للنواة | صفر |
| مطابقة وحدات المصدر مع wheel المختبر | كل الوحدات متطابقة بالهاش |
| فحص build / twine | wheel وsdist ناجحان |
| المنصة المثبتة بالتنفيذ | Python 3.12.3 / Linux / CPU |

الأعداد متداخلة وليست 282 ميزة مستقلة. اختبارات النماذج عمال معزولة متسلسلة
لتجنب نفاد الذاكرة؛ ليس تشغيل كل المحركات في process واحدة. المارك contract
والfixture لا يعنيان نموذجاً مزيفاً؛ لكن خادم البروتوكول المرجعي ليس daemon المزود.
التقارير القديمة محفوظة للتاريخ ولا تمثل أرقام هذا الإصدار. سجلات XML وJSON في
reports/verification-workers-0.3 وpytest-0.3.xml وcoding-guide-verification.json.

## ما اكتمل فعلياً
- بوابة AI وصف مختصر وخدمة صريحة ومفاتيح اختيار model/backend/endpoint/device.
نموذج محلي افتراضي للنص العام، جلسة Model قابلة لإعادة الاستخدام، إظهار backend
والأخطاء والتوقيت اختيارياً، لا تخمين أهداف تدريب/مراجع جودة/إذن جهاز.
- environment وmodel_plan يفحصان hints وRAM/cgroup وnvidia-smi المتاح ويقدران حجم
الأوزان؛ تحقق CPU ورفض CUDA غير الموجود. لا تقدير fit مضمون أو offload آلي.
- NLP عربي: تطبيع وتجزئة واشتقاق ISRI ومشروعات تصنيف TF-IDF/LogisticRegression
وتقييم وحفظ/استعادة، LDA للمواضيع، تشابه لفظي، وتضمين متعدد اللغات فعلي منفصل.
- بيانات وأعمال: تنظيف وتجميع وتحليل CSV، تنبؤ شهري متحقق زمنياً، توصيات، مطابقة
دفاتر Decimal وإخفاء أنماط بريد/هاتف تقريبياً. لا ضمان جودة قرارات مالية/سريرية.
- مصنع: خصائص حساسات وأطياف بتردد عينة، SPC بمرجع مستقل، عائد إنتاج، تقييم مصنف
صيانة بتسميات، وفحص فروق صورة مرجعية مصطفة. ليست عيوباً صناعية عامة أو RUL.
- تشغيل أوزان SmolLM2-135M وMiniLM متعدد اللغات وWhisper-tiny وMobileNet وSSDlite
وLRASPP. تحليل وجوه/كائنات/تصنيف/تقسيم ومناطق حركة وتتبع مؤقت، OCR عربي/إنجليزي،
تفريغ صوتي وملف كلام espeak-ng، وتدريب شبكة PyTorch وحفظ safetensors.
- ONNX CPU استدلال حقيقي، TensorFlow تدريب حفظ/استدلال في الاختبار واستدلال نموذج
Keras محلي ضمن API، ومحاولات توليد/إصلاح أكواد واختبارات بنموذج محلي مع مراجعة
نحوية؛ لا ادعاء أن كل كود مولد صحيح أو آمن أو أنه أُصلح بنجاح منطقي.
- مستندات TXT/PDF/DOCX/XLSX، معلومات/بحث واستخراج، RAG وFAISS/SQLite ومصادر، وكلاء
بأدوات مسموحة وDAG وجدولة عند tick، SQLite read-only وAPI محدودة بمفتاح، A-star.
- MQTT مع وسيط حقيقي وSerial PTY وModbus مع خادم محلي؛ شبكات برمجية فعلية لا عتاد
روبوت/PLC. compatible وOllama protocols مع خادم مرجعي يستدل بنموذج حقيقي.

## ملفات التوثيق والتجهيز
USER_GUIDE_AR.md وUSER_GUIDE_EN.md دليلان ممتلئان بالتثبيت والأمثلة والمتطلبات
والنشر وحل الأخطاء. ALFAROUQ_AI_COMPLETE_CODING_GUIDE.md يضم 64 مدخلاً و61 كتلة
منفذة مع مقتطف ناتج. examples/guide يشمل ملفات تشغيل مستقلة للكتل. دليل المالك
ALFAROUQ_AI_OWNER_MASTER_GUIDE_AR.md خاص ويشرح الوحدات والملفات والواجهات والتبعيات
والرخص والبناء والتشخيص. له نسخة HTML محلية لقراءة الهاتف؛ كلاهما مستبعد من
staging النشر العام وsdist. README وHTML وCI وقوالب المساهمة/الأمان/النشر جاهزة.
CI مصفوفة مستقبلية، لا دليل أن GitHub Actions أو Windows/macOS اشتغلت هنا.

## غير مثبت أو غير مكتمل
image.objects القديم وimage.generate وvideo.generate محولات موجودة لكن غير
مختبرة بأوزان فعلية. لا نتائج توليد صور/فيديو مرفقة كأنها إنجاز. لا تشغيل GPU
حقيقي أو multi-GPU/tensor parallel/quantization ضخم أو معماريات HF عشوائية، لا
اختبار فعلي لـvLLM/Ollama الأصليين أو Hugging Face Spaces/Colab/Kaggle/Codespaces،
لا أجهزة مصنع/روبوت حقيقية، لا Fine-tuning واسع، لا تصديق دقة عامة، لا تقييم
Arabic benchmark شامل، ولا أمان/توسع إنتاجي/امتثال طبي أو مصرفي. الأوزان ليست
داخل ZIP؛ تحميلها اختياري بعد الموافقة ومراجعة حقوقها ومساحة/عتاد التشغيل.
فهم الطلب routing محافظ مع fallback نصي؛ ليس تنفيذ أي طلب مستحيل بلغة طبيعية.

## النشر والنسخ والحقوق
لم تتوفر جلسة GitHub مخولة (فشل gh auth status) ولا OAuth Google Drive أو token
خاص بالتطبيق. لم ينشر شيء على GitHub/PyPI/Hugging Face أو Google Drive، ولا توجد
روابط عامة مخترعة. أدوات النشر جافة افتراضياً ومهيأة لتسجيل المالك ومراجعته.
AI Drive بديل خاص منفصل إذا نجح الحفظ وتظهر رابطه في رسالة التسليم، لا ادعاء
Google Drive. لا يمكن ضمان أو إلغاء شاشة اشتراك المنصة؛ الأرشيف صغير وسليم
ومسارات تنزيل بديلة تُذكر عند نجاحها فقط. النسخة الأصلية المرفقة تحفظ كاحتياط
مستقل ولا تدمج .git القديمة في الإصدار المنظف.

حقوق التأليف لخالد سلمان. وفق أحدث طلب للنشر المفتوح الكود الأصلي Apache-2.0؛
هذا يمنح حقوقاً للجمهور وفق الرخصة ولا يساوي All Rights Reserved مطلقاً. الصورة
والهوية بشروط مستقلة والمكونات/الأوزان الخارجية تحت تراخيصها. لم تُنقل ملكية
أي مكتبة خارجية. لا استشارة قانونية. صورة المؤسس الأصلية محفوظة بهاشها دون تعديل.

## التشغيل السريع
فك ZIP وافتح المجلد الذي فيه pyproject.toml، أنشئ venv ثم
`python -m pip install .` أو ثبت wheel من dist. افتح USER_GUIDE_AR.html للشرح.
على الهاتف اقرأ HTML أو Markdown وافتح Colab في المتصفح للحساب عند الحاجة؛
لا وعد أن Android يشغّل كل المحركات محلياً. لا أوزان أو مفاتيح في الأرشيف.
سلامة CRC وفك الأرشيف وهاش كل ملف تُسجل في verification-receipt.json وmanifest
بعد بناء ZIP؛ لا تساوي هذه الفحوص جودة تنبؤ أو أمان نموذج خارجي.
'''
    (ROOT/'reports/RELEASE_REPORT.ar.md').write_text(ar)
    (ROOT/'reports/RELEASE_REPORT.en.md').write_text('''# AlFarouq AI 0.3.0a1 — measured release report
Date: 2026-11-19. Copyright Khalid Salman.
64 registered services, 133 installed-wheel tests passed (zero failures/errors/skips),
88 dependency-light tests passed (45 deliberately deselected), 61 exact guide examples
executed successfully against the installed wheel. Counts overlap. Zero mandatory
runtime dependencies. Python 3.12.3/Linux/CPU only; isolated sequential model workers.
All shipped module sources match the tested wheel. Build and twine pass.
User guides: USER_GUIDE_AR.md and USER_GUIDE_EN.md. Complete reference includes every
service, executed snippets and output previews. Private owner guide excluded from
public staging and source distribution. Founder photo preserved unchanged.
Actual trained weights: SmolLM2, multilingual MiniLM, Whisper tiny, MobileNet, SSDlite,
LRASPP. OCR/TTS, Torch training, Keras training/inference, ONNX runtime, industrial
local transports and real-model HTTP reference protocols exercised. Reference server
is not actual vendor vLLM/Ollama deployment; PTY/server tests are not physical devices.
image.objects legacy/image.generate/video.generate actual-weight inference unverified.
No GPU/multi-GPU/quantization or cloud-platform runtime validation, general Arabic
quality benchmark, production security audit, clinical/banking/safety certification,
or universal arbitrary-model/task execution. Small-model code outputs are untrusted.
No weights, secrets or Git history bundled. No public GitHub/PyPI/HF publication and
no authorized Google Drive upload occurred. AI Drive is separate and is linked only
if a storage operation actually succeeds. Platform billing rules cannot be bypassed.
Original code Apache-2.0, copyright retained; founder identity/photo and external
libraries/models/datasets have independent terms. See the Arabic report for details,
release-verification-0.3.json for evidence and the final archive receipt for integrity.
''')
    owner=ROOT/'ALFAROUQ_AI_OWNER_MASTER_GUIDE_AR.md'
    if owner.exists():
        import markdown
        body=markdown.markdown(owner.read_text(),extensions=['fenced_code','tables'])
        (owner.with_suffix('.html')).write_text('<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>دليل المالك الخاص — AlFarouq AI</title><style>body{font:17px/1.9 system-ui;max-width:1000px;margin:auto;padding:24px;color:#123}pre{direction:ltr;text-align:left;overflow:auto;background:#edf3f5;padding:16px}code{direction:ltr}table{display:block;overflow:auto}h1,h2{color:#075c65}</style><body>'+body+'</body></html>')
    print(json.dumps({'version':__version__,'tests':counts,'examples':len(guide['examples']),'modules_match':all(matches.values()),'core_tests':coretests,'report_ready':True},indent=2))
if __name__=='__main__':main()
