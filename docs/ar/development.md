> هذا المحتوى محفوظ من 0.1.0. الحالة الحالية في [كتاب 0.2](handbook-0.2.md) و[مصفوفة 0.2](capabilities-0.2.md).

# التطوير والإضافات والإصدار
[English](../en/development.md) · [المساهمة](../../CONTRIBUTING.md)

## إضافة قدرة حقيقية
```python
from alfarouqai import Client, Capability, Result

def count_words(*, text, config):
    return Result('custom.words', {'count':len(text.split())}, 'my-plugin')

client = Client()
client.registry.register(Capability('custom.words', count_words, 'Word count', ('text',)))
print(client.run('custom.words', text='Hello AlFarouq AI').data)
```
الدالة معلنة المدخلات، لا تثبت مكتبات خفياً، وتعيد Result، وتختبر بمدخلات حقيقية
وتوثيق عربي/إنجليزي. الأسماء المكررة والمدخلات غير المعروفة مرفوضة.
يمكن لحزمة منفصلة إعلان `[project.entry-points."alfarouqai.plugins"]` ثم
`counter = "my_plugin:register"` حيث register(registry) تسجل Capability.
`client.registry.load_plugins(consent=True)` يحمل إضافات مثبتة موثوقة فقط.
تحميل إضافة يشغل Python بصلاحيات العملية؛ ليس sandbox.

## اختبارات وبناء محلي
```bash
python -m pip install -e '.[dev,ml,vision,documents]'
python -m pytest
python -m build
python -m twine check dist/*
```
اختبار PDF ينشئ عينة عبر reportlab؛ لتكراره ثبّت reportlab اختيارياً، وإلا
يُتخطى مع بيان صريح. اختبارات model inference الحقيقية غير موجودة بعد.
تقرير بيئة الاختبار ملف جرد بإصدارات مثبتة، لا lock شامل متعدد المنصات ولا
دليل خلو من الثغرات. ملفات GitHub Actions مجهزة ولم تشغّل على GitHub هنا.

## تهيئة GitHub وPyPI دون نشر
المجلد يحتوي القوالب وCI وسياسات المساهمة والأمان وmetadata والحزم المبنية.
لم ينشأ مستودع في حساب خارجي ولم يُحجز اسم ولم يُرفع شيء.
بعد قرار الترخيص والموافقة الصريحة وتوفر الاسم: أنشئ مستودعاً في حسابك، راجع
الصورة والبريد والعمر قبل إتاحتها علناً، ثم اربط المجلد وارفعه. بعد نجاح CI
ابنِ إصداراً جديداً واختبره في TestPyPI باستخدام بيانات اعتمادك ووافق على
الإصدار النهائي. لا توجد رموز سرية ولا publish workflow تلقائي.
لا تفترض أن حق استخدام اسم PyPI أو علامة تجارية قد تم التحقق منه.

تدار النسخ عبر pyproject.toml و__version__ وCHANGELOG. استخدم SemVer مع توضيح
أن 0.x تجريبي. لا تقبل مساهمات من الغير دون شروط مكتوبة متوافقة مع اختيار
المالك الحالي. لا يجوز وضع MIT فوق أعمال أصلية مع طلب منع إعادة استخدامها.
