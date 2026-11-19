"""Build the offline documentation. Requires optional build tool: pip install Markdown.

Run from checkout with an installed AlFarouq package (or PYTHONPATH=src).
No network/AI calls, remote assets, or publication are performed.
"""
from pathlib import Path
import html
import inspect
import re
import sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    try:
        import markdown
    except ImportError:
        raise SystemExit('Documentation build tool missing: python -m pip install Markdown')
    from alfarouqai import Client
    client=Client()
    for lang in ('ar','en'):
        intro = '# مرجع API\n\nالتواقيع التالية مولدة من الكود الحقيقي. Config مدخلة بواسطة Client.\n' if lang=='ar' else '# API reference\n\nSignatures generated from actual handlers. Client supplies Config.\n'
        parts=[intro, '[Guide](guide.md) · [Capabilities](capabilities.md)\n', '```python\nAI(prompt, *, config=None, **inputs) -> Result\nClient(config=None, registry=None)\nClient.run(task, **inputs) -> Result\nClient.plan(prompt, **inputs) -> dict\nClient.train(data=..., target=..., problem=...) -> TrainedModel\nResult.export(path, *, overwrite=False) -> Path\nKnowledgeBase(chunk_size=800, overlap=100)\nAgentTeam(client=None, allowed_tasks=None, workers=1)\n```\n']
        for item in client.capabilities():
            cap=client.registry.get(item['name'])
            params=[name+'='+(repr(p.default) if p.default is not inspect.Parameter.empty else '...') for name,p in inspect.signature(cap.handler).parameters.items() if name not in ('kwargs','config')]
            parts += [f'## `{cap.name}`\n', cap.description+'\n', '```python\nclient.run('+repr(cap.name)+', '+', '.join(params)+')\n```\n', f'Extra: `{cap.extra or "core"}`. Required: `{", ".join(cap.required) or "see handler input rules"}`.\n']
        parts += ['## Errors / الأخطاء\n\n`ValidationError`, `MissingDependency`, `ConsentRequired`, `UnsupportedTask` inherit `AlFarouqError`. Some engine exceptions propagate; check the guide and security policy.\n', '## Model adapter limits / حدود النماذج\n\nSee the current capability-verification report for actual trained-weight tests versus experimental/legacy adapter-only paths.\n']
        (ROOT/f'docs/{lang}/api.md').write_text('\n'.join(parts),encoding='utf-8')
    paths = list((ROOT/'docs').rglob('*.md')) + [ROOT/'README.md',ROOT/'README.ar.md',ROOT/'THIRD_PARTY_NOTICES.md',ROOT/'SECURITY.md',ROOT/'CONTRIBUTING.md',ROOT/'USER_GUIDE_AR.md',ROOT/'USER_GUIDE_EN.md',ROOT/'ALFAROUQ_AI_COMPLETE_CODING_GUIDE.md'] + list((ROOT/'reports').glob('*.md'))
    style='body{font:17px/1.85 system-ui,sans-serif;max-width:1080px;margin:0 auto;padding:32px;background:#fafcff;color:#16243b}a{color:#075f94}pre,code{direction:ltr;text-align:left;font-family:monospace}pre{overflow:auto;padding:22px;border-radius:12px;background:#0d2235;color:#e0f4ff}code{font-size:.9em}table{border-collapse:collapse;width:100%;display:block;overflow:auto}td,th{border:1px solid #cbd5e1;padding:10px;text-align:start}th{background:#e2eef5}h1,h2{color:#073d57}img{max-width:100%}nav,footer{padding:16px 0;border-bottom:1px solid #cbd5e1}footer{font-size:13px;color:#475569}blockquote{border-inline-start:4px solid #079499;padding-inline-start:1em} @media print{body{font-size:12px}pre{white-space:pre-wrap}}'
    for source in paths:
        arabic = '/ar/' in source.as_posix() or '.ar.' in source.name or source.name=='USER_GUIDE_AR.md'
        body=markdown.markdown(source.read_text(encoding='utf-8'),extensions=['fenced_code','tables','toc'])
        # Only rewrite Markdown links when the corresponding rendered local page exists/is in this build.
        def rewrite(match):
            target=match.group(1)
            base=target.split('#')[0]
            if base.endswith('.md') and (source.parent/base).resolve() in {p.resolve() for p in paths}:
                return 'href="'+target.replace('.md','.html')+'"'
            return match.group(0)
        body=re.sub(r'href="([^"]+)"',rewrite,body)
        target=source.with_suffix('.html')
        import os
        home=Path(os.path.relpath(ROOT/'docs/index.html',target.parent)).as_posix()
        target.write_text(f'<!doctype html><html lang="{"ar" if arabic else "en"}" dir="{"rtl" if arabic else "ltr"}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(source.stem)} | AlFarouq AI</title><style>{style}</style><nav><a href="{home}">AlFarouq AI — Documentation / التوثيق</a></nav><main>{body}</main><footer>© 2026 Khalid Salman — Original code Apache-2.0. Identity and third-party rights are separate. Local alpha; not published.</footer></html>',encoding='utf-8')
    index='''<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AlFarouq AI | خالد سلمان</title>
<style>body{margin:0;background:#071826;color:#e8f2f6;font:17px/1.9 system-ui}main{max-width:1100px;margin:auto;padding:42px 24px}header{padding:35px;border:1px solid #315163;border-radius:22px;background:#102d3c}h1{font-size:52px;margin:0;color:#65e5d0;direction:ltr;text-align:right}h2{color:#83dce4}a{color:#9ae9e3}p{max-width:850px}.badge{display:inline-block;padding:5px 13px;background:#21445b;border-radius:30px;font-size:14px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:20px;margin:28px 0}.card{background:#102938;border:1px solid #294958;border-radius:18px;padding:26px}.founder{display:flex;gap:28px;align-items:center;flex-wrap:wrap}.founder img{width:200px;height:230px;object-fit:cover;object-position:50% 52%;border-radius:18px}code{direction:ltr;display:block;text-align:left;white-space:pre-wrap;background:#071826;padding:16px;border-radius:12px}footer{font-size:14px;color:#adbfca;border-top:1px solid #315163;margin-top:40px;padding-top:20px}</style>
<main><header><span class="badge">0.3.0a1 · Alpha · Local-first · No public release</span><h1>AlFarouq AI</h1><p><a href="../USER_GUIDE_AR.html">دليل المستخدم العربي 0.3</a> · <a href="../USER_GUIDE_EN.html">English user guide 0.3</a> · <a href="../ALFAROUQ_AI_COMPLETE_CODING_GUIDE.html">جميع أمثلة الخدمات</a></p><p><a href="ar/handbook-0.2.html">كتاب الاستخدام 0.2 بالعربية</a> · <a href="en/handbook-0.2.html">0.2 handbook</a> · <a href="ar/curriculum.html">المنهج التعليمي</a></p><p><a href="ar/handbook-0.2.html">كتاب الاستخدام 0.2 بالعربية</a> · <a href="en/handbook-0.2.html">0.2 handbook</a> · <a href="ar/curriculum.html">المنهج التعليمي</a></p><p>بوابة Python موحدة لتبسيط أدوات الذكاء الاصطناعي، مع نواة خفيفة ومحركات اختيارية ونتائج قابلة للتصدير.</p><p lang="en" dir="ltr">One Python entry point. Explicit capabilities, optional local engines, bounded agent workflows and honest provenance.</p><a href="ar/guide.html">ابدأ بالعربية</a> · <a href="en/guide.html">English guide</a> · <a href="../reports/RELEASE_REPORT.ar.html">تقرير التسليم</a></header>
<section class="grid"><article class="card"><h2>ابدأ بسطر واحد</h2><code>from alfarouqai import AI\nr = AI("حلل هذا النص", text="الذكاء الاصطناعي يساعد الطلاب.")\nprint(r.data)</code><p>للمهام المتقدمة استخدم Client.run مع اسم قدرة صريح. لا تنزيل ولا شبكة افتراضية.</p></article><article class="card"><h2>Implementation, not promises</h2><p lang="en" dir="ltr">Real local text, CSV, ML, AST, document, face, motion and retrieval tools. Actual trained-model verification is separated from experimental adapters.</p><a href="ar/capabilities.html">حالة المجالات</a> · <a href="en/capabilities.html">Capability matrix</a></article></section>
<section class="card founder"><img src="../identity/founder/khalid-salman-original.jpg" alt="خالد سلمان — الصورة الأصلية المقدمة"><div><h2>خالد سلمان · Khalid Salman</h2><p>اليمن · 22 عاماً كما قدمه المؤسس<br>التخصص: الذكاء الاصطناعي<br>المجال: هندسة حلول الذكاء الاصطناعي<br>مؤسس AlFarouq AI وصاحب حقوق أعماله الأصلية</p><a href="mailto:khalidsalman7140@gmail.com">khalidsalman7140@gmail.com</a></div></section>
<section class="grid"><article class="card"><h2>التوثيق العربي</h2><p><a href="ar/guide.html">التثبيت والأمثلة خطوة بخطوة</a><br><a href="ar/architecture.html">المعمارية والقرارات</a><br><a href="ar/api.html">مرجع القدرات</a><br><a href="ar/development.html">التطوير والمساهمة والنشر</a></p></article><article class="card" lang="en" dir="ltr"><h2>English documentation</h2><p><a href="en/guide.html">Install and learn</a><br><a href="en/architecture.html">Architecture and decisions</a><br><a href="en/api.html">API reference</a><br><a href="en/development.html">Development and release</a></p></article><article class="card"><h2>أدلة التسليم</h2><p><a href="research/SOURCES.html">مصادر البحث والترخيص</a><br><a href="../reports/RELEASE_REPORT.en.html">English delivery report</a><br><a href="../reports/pytest-0.3.xml">نتائج الاختبارات XML</a><br><a href="../THIRD_PARTY_NOTICES.html">حقوق المكونات الخارجية</a></p></article></section>
<footer><p>© 2026 Khalid Salman. جميع حقوق الأعمال الأصلية محفوظة. الكود الأصلي Apache-2.0؛ حقوق الصورة والهوية مستقلة. تراخيص المكتبات والأعمال الخارجية مستقلة ومحفوظة لأصحابها.</p><p lang="en" dir="ltr">Original source code is Apache-2.0; copyright remains with Khalid Salman. Identity/photo licenses are separate. Owner approval is required for public publication. Founder biography is supplied, not independently verified. No remote fonts, trackers, scripts or assets are required.</p></footer></main></html>'''
    (ROOT/'docs/index.html').write_text(index,encoding='utf-8')
    print('Offline HTML documentation built:',len(paths)+1,'pages')

if __name__=='__main__':
    main()
