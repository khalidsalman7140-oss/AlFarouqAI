# AlFarouq AI 0.3.0a1 — Current release / الإصدار الحالي

[العربية](USER_GUIDE_AR.md) · [English](USER_GUIDE_EN.md) · [All service examples](ALFAROUQ_AI_COMPLETE_CODING_GUIDE.md) · [Current verification](reports/RELEASE_REPORT.ar.md)

Latest original-code license: Apache-2.0. Copyright © 2026 Khalid Salman. Identity/photo and third-party rights are separate. This local alpha is not a published PyPI/GitHub release. Older 0.1/0.2 material below is historical, not the current verification record.

# الإصدار الحالي: 0.2.0 Alpha — تطوير إضافي، دون نشر عام
[الكتاب العربي المحدث](docs/ar/handbook-0.2.md) · [المنهج التعليمي](docs/ar/curriculum.md) · [مصفوفة 0.2](docs/ar/capabilities-0.2.md) · [التقرير الحالي](reports/FINAL_REPORT.ar.md)

النواة ما زالت خفيفة وحقوق خالد سلمان محفوظة. أضيف تشغيل نماذج محلية فعلية.
المحتوى التالي محفوظ من إصدار 0.1.0؛ عبارات حالته التاريخية لا تصف نتيجة 0.2.

---

# AlFarouq AI — الفاروق للذكاء الاصطناعي
**إصدار تأسيسي محلي 0.1.0 / Alpha — لم يُنشر على GitHub أو PyPI.**

[English](README.md) · [الدليل العربي](docs/ar/guide.md) · [صفحة المشروع المحلية](docs/index.html) · [حالة التنفيذ](docs/ar/capabilities.md) · [تقرير التسليم](reports/FINAL_REPORT.ar.md)

## الرؤية
نقطة دخول واحدة إلى أدوات ذكاء اصطناعي محلية قابلة للتوسع، للطلاب والباحثين
ومطوري Python والشركات. البساطة لا تعني اختلاق نتائج: كل نتيجة تحدد المحرك
والتحذيرات ومصدرها. النواة بلا اعتماديات تشغيل إلزامية؛ المحركات الثقيلة اختيارية.
ليست المكتبة نموذجاً موحداً خارقاً ولا بديلاً عن تدريب وتقييم النماذج المتخصصة.

## بدء سريع من المجلد المفكوك
```bash
python -m venv .venv
# Linux / macOS:
source .venv/bin/activate
# Windows PowerShell بدلاً من السطر السابق:
# .venv\Scripts\Activate.ps1
python -m pip install .
python examples/01_quickstart.py
```
لا تستخدم `pip install alfarouqai` من الإنترنت اعتماداً على هذا التسليم؛ الاسم
غير محجوز أو متحقق التوفر. ثبّت من المجلد أو wheel المرفق فقط.

```python
from alfarouqai import AI, Client
result = AI('حلل هذا النص', text='الذكاء الاصطناعي يساعد الطلاب. Python helps developers.')
print(result.data)
result.export('result.json')
client = Client()
print(client.capabilities())
```

للتعلم الآلي: `python -m pip install '.[ml]'` ثم `python examples/02_machine_learning.py`.
لا يحتاج المثال مفتاح API ولا نموذجاً مدفوعاً. بياناته تعليمية مصطنعة وليست دليلاً على جودة بحثية.

## المؤسس والملكية
<img src="identity/founder/khalid-salman-original.jpg" alt="خالد سلمان — الصورة المقدمة من المؤسس" width="180">

الاسم: **خالد سلمان — Khalid Salman**. الدولة: **اليمن**. العمر: **22 عاماً**
كما قدمه المؤسس، دون تحقق مستقل أو تحديث تلقائي. التخصص: **الذكاء الاصطناعي**.
المجال: **هندسة حلول الذكاء الاصطناعي**. اسم المشروع: **AlFarouq AI**.
البريد: [khalidsalman7140@gmail.com](mailto:khalidsalman7140@gmail.com).
الصورة الأصلية محفوظة دون تعديل، ولا تُستخدم لتدريب أي نموذج.

جميع الأكواد والتصميمات والمكونات الأصلية والهوية الخاصة بمشروع AlFarouq AI
مملوكة لخالد سلمان، مؤسس المشروع. لا يُسمح بنسخ أو اقتباس أو إعادة استخدام أو
إعادة توزيع الأعمال الأصلية الخاصة بالمشروع دون إذن كتابي مسبق من المالك.
يجب احترام تراخيص المكتبات والأدوات الخارجية، ولا يجوز ادعاء ملكية أعمال الآخرين.

**تنبيه ترخيص:** التزم هذا التسليم بمنع النسخ المطلوب في [LICENSE](LICENSE).
لذلك ليس مفتوح المصدر وفق تعريف OSI، ولا يمنح الجمهور حق إعادة الاستخدام.
يلزم قرار المالك بشأن ترخيص مفتوح مثل MIT/Apache-2.0 إذا أراد تحقيق هدف
المساهمة العالمية المفتوحة. يمكن الاحتفاظ بحقوق الاسم والصورة والهوية على نحو
منفصل عن ترخيص الكود. هذا توضيح هندسي وليس استشارة قانونية.

## حدود الإصدار
المتاح فعلياً: إحصاءات النصوص وتلخيص استخراجي، CSV، تدريب/تقييم/تنبؤ جدولي،
AST، سجلات دفاعية، مستشعرات مسجلة، استخراج مستندات، وجوه وحركة، استرجاع نصي،
تصدير، إضافات، وخطوط وكلاء محدودة. توجد موصلات محلية للاستدلال اللغوي والصوت
والكشف العام والبحث الدلالي، **لكن لم تُختبر بأوزان فعلية في هذه الجلسة**.
لا تشمل النسخة توليد صور/فيديو، تحويل نص إلى صوت، قيادة روبوتات، أجهزة متصلة،
تتبع أشخاص، تنفيذ أكواد مولدة، أو تعدد وكلاء لغوي مستقل.

[التثبيت والتعلم](docs/ar/guide.md) · [المعمارية](docs/ar/architecture.md) ·
[التوسع والنشر](docs/ar/development.md) · [السياسة الأمنية](SECURITY.md)
