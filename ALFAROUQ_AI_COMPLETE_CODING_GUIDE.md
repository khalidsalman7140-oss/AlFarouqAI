# ALFAROUQ AI COMPLETE CODING GUIDE
## الدليل العملي الشامل — 0.3.0a1
تاريخ التحقق: 2026-11-19. الكود الحالي Apache-2.0؛ حقوق المؤلف لخالد سلمان من اليمن.

### ما المكتبة وما حدودها؟
بوابة Python محلية أولاً لأدوات AI وتحليل البيانات وخدمات عملية. تعيد نتائج
حقيقية مع backend وتحذيرات ومصدر، ولا تخلق عتاداً أو دقة أو صلاحية قانونية.
كل مثال خدمة قابل للتشغيل أدناه نُفذ من النص نفسه، وسجله ومخرجاته في
reports/coding-guide-results. ثلاثة موصلات غير مختبرة مفصولة بلا مثال نجاح وهمي.

## التثبيت والإعداد
من المجلد المفكوك أنشئ بيئة: `python -m venv .venv` ثم فعلها بالطريقة المناسبة
لنظامك: `.venv\Scripts\Activate.ps1` في PowerShell أو `source .venv/bin/activate`
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
كل مثال كامل محفوظ أيضاً تحت examples/guide، ويمكن تشغيله من Terminal من جذر
المشروع. في Jupyter/Colab/Kaggle ثبّت wheel ثم ارفع المصدر لأدوات الأمثلة واضبط
current directory إلى جذر المشروع، ثم شغّل التهيئة والكتلة نفسها. هذا تعليم
تشغيل، لا ادعاء أن المنصات السحابية نفذت في التحقق المحلي. لملفاتك الخاصة
استبدل DATA/PHOTO بالمسارات التي تملك حق معالجتها؛ الخدمة نفسها غالباً سطر واحد.

## جميع الخدمات الفعلية
### 1. `text.analyze`

Extractive Arabic/English text statistics and summary

**المتطلبات:** `core/system`. **المدخلات:** `text`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('text.analyze', text='الذكاء الاصطناعي يساعد الطلاب. Python helps researchers.')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.frequency",
  "data": {
    "characters": 56,
    "words": 7,
    "sentences": 2,
    "keywords": [
      [
        "الذكاء",
        1
      ],
      [
        "الاصطناعي",
        1
      ]
    ],
    "extractive_summary": "الذكاء الاصطناعي يساعد الطلاب. Python helps researchers."
  },
  "warnings": [
    "Extractive statistics only; not an LLM or sentiment model."
  ]
}
```

**Terminal:** `python examples/guide/text_analyze.py` من جذر المشروع.

### 2. `data.profile`

Profile a UTF-8 CSV with missing values and numeric statistics

**المتطلبات:** `core/system`. **المدخلات:** `data`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('data.profile', data=DATA/'numeric.csv')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.csv",
  "data": {
    "row_count": 100,
    "columns": {
      "x": {
        "missing": 0,
        "unique": 10,
        "type": "numeric",
        "min": 0.0,
        "max": 9.0
      },
      "y": {
        "missing": 0,
        "unique": 10,
        "type": "numeric",
        "min": 0.0,
        "max": 9.0
      },
      "target": {
        "missing": 0,
        "unique": 2,
        "type": "numeric",
        "min": 0.0,
        "max": 1.0
      }
    },
    "rows": [
      {
        "x": "0",
        "y": "0",
        "target": "0"
      },
      {
        "x": "1",
        "y": "0",
        "target": "0"
      }
    ]
  },
  "warnings": []
}
```

**Terminal:** `python examples/guide/data_profile.py` من جذر المشروع.

### 3. `ml.train`

Train/test a RandomForest with explicit target/problem

**المتطلبات:** `ml`. **المدخلات:** `data, target, problem`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('ml.train', data=DATA/'numeric.csv', target='target', problem='classification')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "scikit-learn.RandomForest",
  "data": {
    "problem": "classification",
    "target": "target",
    "features": [
      "x",
      "y"
    ],
    "numeric_features": [
      "x",
      "y"
    ],
    "train_rows": 75
  },
  "warnings": [
    "Held-out split, not cross-validation. Not suitable evidence for time-series, grouped or causal claims; use domain-specific splits in future versions."
  ]
}
```

**Terminal:** `python examples/guide/ml_train.py` من جذر المشروع.

### 4. `image.analyze`

Local image statistics and frontal face detection

**المتطلبات:** `vision`. **المدخلات:** `image`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('image.analyze', image=PHOTO)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "opencv.HaarCascade",
  "data": {
    "width": 720,
    "height": 1600,
    "channels": 3,
    "mean_rgb": [
      64.36682725694445,
      57.51885243055556
    ],
    "faces": [
      {
        "x": 129,
        "y": 601,
        "width": 506,
        "height": 506
      }
    ]
  },
  "warnings": [
    "Face detection only, not identity recognition or general object detection. Detections can be wrong."
  ]
}
```

**Terminal:** `python examples/guide/image_analyze.py` من جذر المشروع.

### 5. `image.objects`

General object detection using reviewed local model weights

**المتطلبات:** `objects`. **المدخلات:** `image, model_path`.

**غير مثبت باستدلال فعلي:** الموصل القديم يتطلب نموذج Transformers محلياً متوافقاً؛ لم يختبر بأوزان فعلية في هذا الإصدار. البديل vision.detect مختبر ولا يحذف المسار القديم.

### 6. `video.motion`

Bounded frame-difference motion regions

**المتطلبات:** `vision`. **المدخلات:** `video`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
media_fixtures(DATA, PHOTO)
result = ai.run('video.motion', video=DATA/'clip.avi', max_frames=3)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "opencv.frame-difference",
  "data": {
    "fps": 5.0,
    "processed_frames": 3,
    "truncated": false,
    "rows": [
      {
        "frame": 0,
        "time_seconds": 0.0,
        "changed_fraction": 0.0,
        "boxes": []
      },
      {
        "frame": 1,
        "time_seconds": 0.2,
        "changed_fraction": 0.0,
        "boxes": []
      }
    ]
  },
  "warnings": [
    "Motion regions only, not action understanding, person identification or persistent tracking. Camera movement can trigger detections."
  ]
}
```

**Terminal:** `python examples/guide/video_motion.py` من جذر المشروع.

### 7. `audio.info`

PCM WAV metadata

**المتطلبات:** `core/system`. **المدخلات:** `audio`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
media_fixtures(DATA, PHOTO)
result = ai.run('audio.info', audio=DATA/'silence.wav')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.wave",
  "data": {
    "channels": 1,
    "sample_rate": 16000,
    "sample_width_bytes": 2,
    "frames": 16000,
    "duration_seconds": 1.0
  },
  "warnings": []
}
```

**Terminal:** `python examples/guide/audio_info.py` من جذر المشروع.

### 8. `speech.transcribe`

Whisper transcription with an explicit local model

**المتطلبات:** `speech`. **المدخلات:** `audio`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
ai.run('speech.synthesize', text='Hello world. A speech recognition test.', output=OUT/'speech.wav')
result = ai.run('speech.transcribe', audio=OUT/'speech.wav', model_path=str(prepare_model('whisper-tiny')), language='en')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "faster-whisper.cpu-int8",
  "data": {
    "language": "en",
    "text": "The Long World, a speech recognition test.",
    "rows": [
      {
        "start": 0.0,
        "end": 3.0,
        "text": " The Long World, a speech recognition test."
      }
    ]
  },
  "warnings": []
}
```

**Terminal:** `python examples/guide/speech_transcribe.py` من جذر المشروع.

### 9. `document.read`

Extract text from TXT/PDF/DOCX/XLSX

**المتطلبات:** `documents`. **المدخلات:** `document`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('document.read', document=DATA/'note.txt')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.text",
  "data": {
    "text": "AlFarouq AI helps students use Python. Temperature sensors measure heat.\nخالد سلمان مؤسس المشروع. التاريخ 2026-11-16.",
    "characters": 117,
    "rows": []
  },
  "warnings": [
    "Text extraction only; scanned PDFs need OCR, formulas are not recalculated, complex layout may be lost."
  ]
}
```

**Terminal:** `python examples/guide/document_read.py` من جذر المشروع.

### 10. `code.analyze`

Non-executing Python AST and project review

**المتطلبات:** `core/system`. **المدخلات:** `راجع الوظيفة`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('code.analyze', code='import os\nos.system(command)\n')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.ast",
  "data": {
    "parsed_files": 1,
    "rows": [
      {
        "file": "<inline>",
        "lines": 2,
        "imports": [
          "os"
        ],
        "functions": [],
        "classes": []
      }
    ],
    "findings": [
      {
        "file": "<inline>",
        "line": 2,
        "rule": "dangerous-call",
        "message": "Review os.system; untrusted input may execute code"
      }
    ]
  },
  "warnings": [
    "Static heuristic review; not a proof of security. Source code was not executed."
  ]
}
```

**Terminal:** `python examples/guide/code_analyze.py` من جذر المشروع.

### 11. `security.logs`

Defensive authentication log analysis

**المتطلبات:** `core/system`. **المدخلات:** `path`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('security.logs', path=DATA/'auth.log')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.rules",
  "data": {
    "rows": [
      {
        "line": 1,
        "rule": "authentication-failure",
        "source": "192.0.2.10"
      }
    ],
    "failed_auth_by_source": {
      "192.0.2.10": 1
    }
  },
  "warnings": [
    "Defensive, offline heuristic analysis only; no network scanning or exploitation."
  ]
}
```

**Terminal:** `python examples/guide/security_logs.py` من جذر المشروع.

### 12. `iot.analyze`

Offline sensor time-series z-score anomaly flags

**المتطلبات:** `core/system`. **المدخلات:** `data, column`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('iot.analyze', data=DATA/'sensors.csv', column='temperature')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.zscore",
  "data": {
    "mean": 23.425,
    "std": 9.096393516113954,
    "threshold": 3.0,
    "rows": [
      {
        "row": 0,
        "value": 21.0,
        "z_score": -0.26658917027986917,
        "anomaly": false
      },
      {
        "row": 1,
        "value": 22.0,
        "z_score": -0.15665549181394375,
        "anomaly": false
      }
    ]
  },
  "warnings": [
    "Offline sensor analytics; no device is connected and no actuator commands are sent."
  ]
}
```

**Terminal:** `python examples/guide/iot_analyze.py` من جذر المشروع.

### 13. `llm.chat`

Opt-in Ollama text and supported vision chat

**المتطلبات:** `core/system`. **المدخلات:** `prompt`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
with model_server() as origin:
    result = Client(Config(allow_network=True, ollama_url=origin, model='reference-smollm')).run('llm.chat', prompt='What is the capital of France?')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "ollama",
  "data": {
    "text": "The capital of France is Paris.",
    "model": "reference-smollm",
    "done": true
  },
  "warnings": [
    "Generated content may be incorrect. Verify citations and code. Ollama must be configured to avoid cloud-backed aliases."
  ]
}
```

**Terminal:** `python examples/guide/llm_chat.py` من جذر المشروع.

### 14. `local.generate`

Generate text with a local trained causal language model

**المتطلبات:** `local`. **المدخلات:** `prompt`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai('Explain Python briefly.', task='local.generate', max_new_tokens=40)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "transformers.local-causal-lm",
  "data": {
    "text": "Python is a high-level, interpreted programming language that is widely used for web development, data analysis, machine learning, and automation. It is a versatile language that c …",
    "generated_tokens": 40,
    "input_tokens": 29
  },
  "warnings": [
    "Generated content can be wrong. Default 135M model is English-first and limited; not a strongest-model or Arabic-quality claim. Input is truncated to 1024 tokens."
  ]
}
```

**Terminal:** `python examples/guide/local_generate.py` من جذر المشروع.

### 15. `nlp.classify`

Classify supplied text by model likelihood of candidate labels

**المتطلبات:** `local`. **المدخلات:** `text, labels`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('nlp.classify', text='The service was excellent.', labels=['positive','negative'])
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "local-llm.label-likelihood",
  "data": {
    "label": "positive",
    "rows": [
      {
        "label": "positive",
        "relative_score": 0.5228655338287354,
        "mean_log_likelihood": -12.288873672485352
      },
      {
        "label": "negative",
        "relative_score": 0.47713443636894226,
        "mean_log_likelihood": -12.380399703979492
      }
    ]
  },
  "warnings": [
    "Relative scores are not calibrated probabilities; labels are ranked by a small LLM, not a task-finetuned classifier."
  ]
}
```

**Terminal:** `python examples/guide/nlp_classify.py` من جذر المشروع.

### 16. `code.generate`

Generate untrusted Python code suggestions with a local LLM

**المتطلبات:** `local`. **المدخلات:** `prompt`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('code.generate', prompt='Write a Python function add(a,b).', max_new_tokens=60)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "transformers.local-causal-lm",
  "data": {
    "text": "```python\ndef add(a, b):\n    return a + b\n```\n\nThis function uses the built-in `+` operator to add two numbers.",
    "generated_tokens": 36,
    "input_tokens": 42
  },
  "warnings": [
    "Generated content can be wrong. Default 135M model is English-first and limited; not a strongest-model or Arabic-quality claim. Input is truncated to 1024 tokens.",
    "Code is untrusted, not executed or proven correct. Review and test in a separate environment."
  ]
}
```

**Terminal:** `python examples/guide/code_generate.py` من جذر المشروع.

### 17. `code.repair`

Suggest a code repair from supplied code and error

**المتطلبات:** `local`. **المدخلات:** `code, error`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('code.repair', code='def add(a,b)\n return a+b', error='missing colon', max_new_tokens=60)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "transformers.local-causal-lm",
  "data": {
    "text": "def add(a,b):\n    return a+b\n\nprint(add(1,2))",
    "generated_tokens": 23,
    "input_tokens": 58
  },
  "warnings": [
    "Generated content can be wrong. Default 135M model is English-first and limited; not a strongest-model or Arabic-quality claim. Input is truncated to 1024 tokens.",
    "Suggested repair only; original files are not modified and correctness is not guaranteed."
  ]
}
```

**Terminal:** `python examples/guide/code_repair.py` من جذر المشروع.

### 18. `code.test`

Run trusted unittest files with explicit OS-execution consent

**المتطلبات:** `core/system`. **المدخلات:** `path`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('code.test', path=DATA/'trusted_tests', consent=True)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "python.unittest.subprocess",
  "data": {
    "returncode": 0,
    "passed": true,
    "timed_out": false,
    "log": "test_add (test_math.T.test_add) ... ok\n\n----------------------------------------------------------------------\nRan 1 test in 0.000s\n\nOK\n"
  },
  "warnings": [
    "Trusted-code runner only. Isolation flag and timeout do NOT block network/filesystem access or child-process side effects."
  ]
}
```

**Terminal:** `python examples/guide/code_test.py` من جذر المشروع.

### 19. `document.summarize`

Summarize extracted document text with a local trained LLM

**المتطلبات:** `local`. **المدخلات:** `document`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('document.summarize', document=DATA/'note.txt', max_new_tokens=50)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "transformers.local-causal-lm",
  "data": {
    "text": "AlFarouq AI helps students use Python. Temperature sensors measure heat.\nخالد سلمان مؤسس المشروع. التاريخ 2026",
    "generated_tokens": 50,
    "input_tokens": 109
  },
  "warnings": [
    "Generated content can be wrong. Default 135M model is English-first and limited; not a strongest-model or Arabic-quality claim. Input is truncated to 1024 tokens.",
    "Only first 12000 characters supplied; LLM token cap can truncate further. Not guaranteed faithful."
  ]
}
```

**Terminal:** `python examples/guide/document_summarize.py` من جذر المشروع.

### 20. `vision.detect`

Detect COCO objects with pretrained TorchVision SSDlite

**المتطلبات:** `torchvision`. **المدخلات:** `image`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('vision.detect', image=PHOTO)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "torchvision.ssdlite320-coco",
  "data": {
    "rows": [
      {
        "label": "person",
        "label_id": 1,
        "score": 0.90146404504776,
        "box_xyxy": [
          4.11,
          417.11
        ]
      }
    ]
  },
  "warnings": [
    "Object detections are uncertain, not identity recognition. COCO category coverage is limited."
  ]
}
```

**Terminal:** `python examples/guide/vision_detect.py` من جذر المشروع.

### 21. `vision.classify`

Classify images with pretrained MobileNet V3

**المتطلبات:** `torchvision`. **المدخلات:** `image`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('vision.classify', image=PHOTO, top_k=3)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "torchvision.mobilenet-v3-small",
  "data": {
    "rows": [
      {
        "label": "sunglass",
        "score": 0.33679741621017456
      },
      {
        "label": "sunglasses",
        "score": 0.18979160487651825
      }
    ]
  },
  "warnings": [
    "ImageNet labels are not a universal image understanding vocabulary."
  ]
}
```

**Terminal:** `python examples/guide/vision_classify.py` من جذر المشروع.

### 22. `vision.segment`

Export a semantic class mask with pretrained LRASPP

**المتطلبات:** `torchvision`. **المدخلات:** `image, output`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('vision.segment', image=PHOTO, output=OUT/'mask.png')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "torchvision.lraspp-voc",
  "data": {
    "mask_path": "/tmp/tmp6hvgesbh/outputs/mask.png",
    "width": 720,
    "height": 1600,
    "rows": [
      {
        "class_id": 0,
        "label": "__background__",
        "pixels": 713433
      },
      {
        "class_id": 15,
        "label": "person",
        "pixels": 438567
      }
    ]
  },
  "warnings": [
    "Semantic class mask (pixel values are class IDs), not individual-instance segmentation."
  ]
}
```

**Terminal:** `python examples/guide/vision_segment.py` من جذر المشروع.

### 23. `vision.ocr`

Recognize printed text with installed Tesseract language models

**المتطلبات:** `core/system`. **المدخلات:** `image`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
media_fixtures(DATA, PHOTO)
result = ai.run('vision.ocr', image=DATA/'ocr.png', language='eng')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "tesseract.system",
  "data": {
    "text": "ALFAROUQ Al 2026",
    "rows": [
      {
        "text": "ALFAROUQ",
        "confidence": 92.66124,
        "x": 20,
        "y": 47,
        "width": 225
      },
      {
        "text": "Al",
        "confidence": 95.619019,
        "x": 261,
        "y": 48,
        "width": 36
      }
    ],
    "language": "eng"
  },
  "warnings": [
    "Recognition depends on scan quality and installed language packs; Arabic quality not guaranteed."
  ]
}
```

**Terminal:** `python examples/guide/vision_ocr.py` من جذر المشروع.

### 24. `video.track`

Detect objects and associate temporary track IDs across video

**المتطلبات:** `torchvision`. **المدخلات:** `video`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
media_fixtures(DATA, PHOTO)
result = ai.run('video.track', video=DATA/'clip.avi', max_frames=3)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "torchvision.ssdlite+centroid-tracker",
  "data": {
    "rows": [
      {
        "frame": 0,
        "time_seconds": 0.0,
        "objects": [
          {
            "label": "person",
            "label_id": 1,
            "score": 0.9135314226150513,
            "box_xyxy": [
              2.08,
              206.75
            ],
            "track_id": 1
          }
        ]
      },
      {
        "frame": 1,
        "time_seconds": 0.2,
        "objects": [
          {
            "label": "person",
            "label_id": 1,
            "score": 0.9398543238639832,
            "box_xyxy": [
              1.73,
              207.22
            ],
            "track_id": 1
          }
        ]
      }
    ],
    "truncated": false,
    "processed_frames": 3
  },
  "warnings": [
    "Temporary same-class centroid tracks; can swap IDs under occlusion/crossing. Not action recognition or identity."
  ]
}
```

**Terminal:** `python examples/guide/video_track.py` من جذر المشروع.

### 25. `speech.recognize`

Transcribe speech with local CTranslate2 Whisper weights

**المتطلبات:** `speech`. **المدخلات:** `audio`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
ai.run('speech.synthesize', text='Hello world. A speech recognition test.', output=OUT/'speech.wav')
result = ai.run('speech.recognize', audio=OUT/'speech.wav', language='en')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "faster-whisper.cpu-int8",
  "data": {
    "language": "en",
    "text": "The Long World, a speech recognition test.",
    "rows": [
      {
        "start": 0.0,
        "end": 3.0,
        "text": " The Long World, a speech recognition test."
      }
    ]
  },
  "warnings": []
}
```

**Terminal:** `python examples/guide/speech_recognize.py` من جذر المشروع.

### 26. `speech.synthesize`

Synthesize an audible WAV using external espeak-ng

**المتطلبات:** `core/system`. **المدخلات:** `text, output`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('speech.synthesize', text='Hello world.', output=OUT/'speech.wav', voice='en-us')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "espeak-ng.system",
  "data": {
    "audio_path": "/tmp/tmplj86bmcy/outputs/speech.wav",
    "voice": "en-us",
    "channels": 1,
    "sample_rate": 22050,
    "sample_width_bytes": 2
  },
  "warnings": [
    "Classical speech synthesis, not neural natural-voice cloning. Voice availability/languages depend on installed executable. External executable license remains independent."
  ]
}
```

**Terminal:** `python examples/guide/speech_synthesize.py` من جذر المشروع.

### 27. `deep.train`

Train and evaluate a real multilayer PyTorch network

**المتطلبات:** `deep`. **المدخلات:** `data, target, problem`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('deep.train', data=DATA/'numeric.csv', target='target', problem='classification', epochs=30)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "pytorch.cpu-mlp",
  "data": {
    "problem": "classification",
    "features": [
      "x",
      "y"
    ],
    "hidden_layers": [
      32,
      16
    ],
    "epochs": 30,
    "initial_loss": 0.6771047115325928
  },
  "warnings": [
    "Small tabular MLP, not universal deep-learning/finetuning. Random split, not time/group aware."
  ]
}
```

**Terminal:** `python examples/guide/deep_train.py` من جذر المشروع.

### 28. `data.forecast`

Fit a linear time trend with chronological validation

**المتطلبات:** `ml`. **المدخلات:** `data, column`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('data.forecast', data=DATA/'sensors.csv', column='temperature', horizon=3)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "numpy.linear-trend",
  "data": {
    "holdout_mae": 5.861162023460413,
    "rows": [
      {
        "step": 1,
        "prediction": 24.676923076923067
      },
      {
        "step": 2,
        "prediction": 24.737992495309562
      }
    ]
  },
  "warnings": [
    "Linear trend baseline, not seasonal forecasting. Input CSV row order is treated as time. Chronological 80/20 holdout."
  ]
}
```

**Terminal:** `python examples/guide/data_forecast.py` من جذر المشروع.

### 29. `data.recommend`

Recommend unseen items using collaborative cosine similarity

**المتطلبات:** `ml`. **المدخلات:** `data, user, user_column, item_column, rating_column`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('data.recommend', data=DATA/'ratings.csv', user='u1', user_column='user', item_column='item', rating_column='rating')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "numpy.user-cosine-collaborative-filtering",
  "data": {
    "rows": [
      {
        "item": "c",
        "score": 4.999999999993657
      }
    ]
  },
  "warnings": [
    "Small-data collaborative baseline, no cold-start or fairness guarantees."
  ]
}
```

**Terminal:** `python examples/guide/data_recommend.py` من جذر المشروع.

### 30. `security.anomalies`

Detect multivariate anomalies with IsolationForest

**المتطلبات:** `ml`. **المدخلات:** `data, columns`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('security.anomalies', data=DATA/'sensors.csv', columns=['time','temperature'])
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "sklearn.IsolationForest",
  "data": {
    "rows": [
      {
        "row": 0,
        "anomaly": true,
        "decision_score": -0.03739177628545154
      },
      {
        "row": 1,
        "anomaly": false,
        "decision_score": 0.0012024764228415474
      }
    ]
  },
  "warnings": [
    "Unsupervised anomalies are not proof of a cyberattack."
  ]
}
```

**Terminal:** `python examples/guide/security_anomalies.py` من جذر المشروع.

### 31. `rag.index`

Extract a document and persist multilingual semantic embeddings

**المتطلبات:** `vector`. **المدخلات:** `document, store`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('rag.index', document=DATA/'note.txt', store=OUT/'knowledge.sqlite')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "sentence-transformers+sqlite",
  "data": {
    "chunks_added": 1,
    "store": "/tmp/tmpsvhkvm96/outputs/knowledge.sqlite"
  },
  "warnings": []
}
```

**Terminal:** `python examples/guide/rag_index.py` من جذر المشروع.

### 32. `rag.search.semantic`

Search persisted semantic vectors with FAISS and source offsets

**المتطلبات:** `vector`. **المدخلات:** `query, store`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
ai.run('rag.index', document=DATA/'note.txt', store=OUT/'knowledge.sqlite')
result = ai.run('rag.search.semantic', query='measuring temperature', store=OUT/'knowledge.sqlite')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "sentence-transformers+faiss+sqlite",
  "data": {
    "query": "measuring temperature",
    "rows": [
      {
        "id": 1,
        "source": "/tmp/tmp250puhr0/data/note.txt",
        "start": 0,
        "end": 117,
        "text": "AlFarouq AI helps students use Python. Temperature sensors measure heat.\nخالد سلمان مؤسس المشروع. التاريخ 2026-11-16."
      }
    ]
  },
  "warnings": [
    "Cosine score is not a calibrated confidence or truth probability."
  ]
}
```

**Terminal:** `python examples/guide/rag_search_semantic.py` من جذر المشروع.

### 33. `rag.answer`

Generate a source-returning answer from semantic retrieval

**المتطلبات:** `vector`. **المدخلات:** `question, store`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
ai.run('rag.index', document=DATA/'note.txt', store=OUT/'knowledge.sqlite')
result = ai.run('rag.answer', question='What measures heat?', store=OUT/'knowledge.sqlite', min_score=.1)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "transformers.local-causal-lm",
  "data": {
    "text": "خالد سلمان مؤسس المشروع. التاريخ 2026-11-16.",
    "generated_tokens": 42,
    "input_tokens": 144,
    "sources": [
      {
        "id": 1,
        "source": "/tmp/tmp1ppknzdd/data/note.txt",
        "start": 0,
        "end": 117,
        "text": "AlFarouq AI helps students use Python. Temperature sensors measure heat.\nخالد سلمان مؤسس المشروع. التاريخ 2026-11-16."
      }
    ],
    "abstained": false
  },
  "warnings": [
    "Generated content can be wrong. Default 135M model is English-first and limited; not a strongest-model or Arabic-quality claim. Input is truncated to 1024 tokens.",
    "Citation presence and factual entailment are NOT guaranteed. Verify against returned sources."
  ]
}
```

**Terminal:** `python examples/guide/rag_answer.py` من جذر المشروع.

### 34. `agents.llm`

Use a local LLM to rank allowed tools and review actual results

**المتطلبات:** `local`. **المدخلات:** `goal, inputs_by_task`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('agents.llm', goal='Analyze text statistics.', inputs_by_task={'text.analyze':{'text':'Python helps students.'}})
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "local-llm-constrained-planner+tools+reviewer",
  "data": {
    "results": {
      "text.analyze": {
        "task": "text.analyze",
        "data": {
          "characters": 22,
          "words": 3,
          "sentences": 1,
          "keywords": [
            [
              "python",
              1
            ],
            [
              "helps",
              1
            ]
          ],
          "extractive_summary": "Python helps students."
        },
        "backend": "stdlib.frequency",
        "warnings": [
          "Extractive statistics only; not an LLM or sentiment model."
        ],
        "provenance": {
          "library_version": "0.3.0a1",
          "elapsed_seconds": 0.000581,
          "network_policy": "explicit opt-in",
          "executed": true
        }
      }
    },
    "trace": [
      {
        "role": "llm-planner",
        "ranking": {
          "label": "Extractive Arabic/English text statistics and summary",
          "rows": [
            {
              "label": "Extractive Arabic/English text statistics and summary",
              "relative_score": 0.5684041380882263,
              "mean_log_likelihood": -5.793736934661865
            },
            {
              "label": "Finish without using another tool",
              "relative_score": 0.43159589171409607,
              "mean_log_likelihood": -6.069079875946045
            }
          ]
        },
        "step": 0
      },
      {
        "role": "specialist",
        "task": "text.analyze",
        "executed": true
      }
    ],
    "review": "\"Text.analyze\" analyzes text statistics and provides a summary of the results.\n\n\"backend\" is a synonym for \"standard library.\"\n\n\"verification\" is not a valid term in this context.\n …",
    "completed_tools": 1
  },
  "warnings": [
    "Planner and reviewer share one small local model. Roles are not independent trained agents. No arbitrary tool generation/execution; review can be wrong."
  ]
}
```

**Terminal:** `python examples/guide/agents_llm.py` من جذر المشروع.

### 35. `automation.tick`

Run due persisted local jobs once when the caller ticks

**المتطلبات:** `core/system`. **المدخلات:** `store`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
scheduler = Scheduler(OUT/'jobs.sqlite')
scheduler.add('one','text.analyze',{'text':'Hello'},run_at=0)
scheduler.close()
result = ai.run('automation.tick', store=OUT/'jobs.sqlite')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "sqlite.caller-driven-scheduler",
  "data": {
    "rows": [
      {
        "id": "one",
        "status": "completed",
        "result": {
          "task": "text.analyze",
          "data": {
            "characters": 5,
            "words": 1,
            "sentences": 1,
            "keywords": [
              [
                "hello",
                1
              ]
            ],
            "extractive_summary": "Hello"
          },
          "backend": "stdlib.frequency",
          "warnings": [
            "Extractive statistics only; not an LLM or sentiment model."
          ],
          "provenance": {
            "library_version": "0.3.0a1",
            "elapsed_seconds": 0.000465,
            "network_policy": "explicit opt-in",
            "executed": true
          }
        }
      }
    ]
  },
  "warnings": [
    "At-most-once job claiming; a crash can leave running jobs unresolved. No daemon, recurrence or background execution is implied."
  ]
}
```

**Terminal:** `python examples/guide/automation_tick.py` من جذر المشروع.

### 36. `iot.mqtt.publish`

Publish an explicitly approved MQTT message and await broker ACK

**المتطلبات:** `iot`. **المدخلات:** `host, topic, message`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
with broker() as port:
    result = Client(Config(allow_network=True)).run('iot.mqtt.publish', host='127.0.0.1', port=port, topic='demo/readings', message={'temperature':24}, consent=True)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "paho-mqtt.qos1",
  "data": {
    "topic": "demo/readings",
    "bytes": 19,
    "acknowledged": true
  },
  "warnings": [
    "Broker acknowledgement is NOT evidence that a physical device acted successfully."
  ]
}
```

**Terminal:** `python examples/guide/iot_mqtt_publish.py` من جذر المشروع.

### 37. `iot.mqtt.read`

Read real MQTT messages from an explicitly configured broker

**المتطلبات:** `iot`. **المدخلات:** `host, topic`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
with broker() as port:
    def publish():
        import time
        time.sleep(.5)
        Client(Config(allow_network=True)).run('iot.mqtt.publish', host='127.0.0.1', port=port, topic='demo/readings', message='24', consent=True)
    thread = threading.Thread(target=publish); thread.start()
    result = Client(Config(allow_network=True)).run('iot.mqtt.read', host='127.0.0.1', port=port, topic='demo/readings', duration=4)
    thread.join()
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "paho-mqtt.subscribe",
  "data": {
    "rows": [
      {
        "topic": "demo/readings",
        "payload": "24",
        "qos": 1
      }
    ],
    "timed_out": false
  },
  "warnings": [
    "Only messages actually received are returned. Local broker tests do not prove physical sensor integration."
  ]
}
```

**Terminal:** `python examples/guide/iot_mqtt_read.py` من جذر المشروع.

### 38. `robotics.serial`

Exchange bounded data on a caller-approved local serial port

**المتطلبات:** `iot`. **المدخلات:** `port`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

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
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "pyserial.local-port",
  "data": {
    "port": "/dev/pts/0",
    "written_bytes": 4,
    "received_hex": "504f4e47",
    "text": "PONG"
  },
  "warnings": [
    "Raw serial transport only, not robot kinematics/navigation or safety certification. A successful write does not prove an actuator state."
  ]
}
```

**Terminal:** `python examples/guide/robotics_serial.py` من جذر المشروع.

### 39. `image.generate`

Experimental local Stable Diffusion integration

**المتطلبات:** `diffusion`. **المدخلات:** `prompt, model_path, output`.

**غير مثبت باستدلال فعلي:** مسار Stable Diffusion تجريبي غير مختبر بأوزان فعلية ضمن هذه الموارد. لا ندرج مثال توليد تحت وصف مختبر.

### 40. `video.generate`

Experimental local CogVideoX integration

**المتطلبات:** `diffusion`. **المدخلات:** `prompt, model_path, output`.

**غير مثبت باستدلال فعلي:** مسار CogVideoX يتطلب موارد ونموذجاً مناسباً؛ لم يجر استدلال فعلي، لذلك لا يوجد مثال تشغيل مثبت هنا.

### 41. `arabic.process`

Normalize, tokenize and optionally stem Arabic text

**المتطلبات:** `nlp`. **المدخلات:** `text`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.ar('يكتب الطلاب دروس اللغة العربية في المدارس')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "unicode+nltk.ISRI",
  "data": {
    "normalized": "يكتب الطلاب دروس اللغة العربية في المدارس",
    "tokens": [
      "يكتب",
      "الطلاب"
    ],
    "filtered_tokens": [
      "يكتب",
      "الطلاب"
    ],
    "stems": [
      "كتب",
      "طلب"
    ],
    "word_count": 7
  },
  "warnings": [
    "ISRI is heuristic stemming, not context-aware lemmatization, POS, NER or dialect understanding. Normalization can merge distinct spellings; preserve original source."
  ]
}
```

**Terminal:** `python examples/guide/arabic_process.py` من جذر المشروع.

### 42. `nlp.train`

Train and evaluate a labeled Arabic/multilingual text classifier

**المتطلبات:** `ml`. **المدخلات:** `data, text_column, target`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
model = ai.text_train(data=DATA/'corpus.csv', text_column='text', target='label')
result = model.report
print(model.predict(['خدمة ممتازة رائعة']).to_dict())
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "sklearn.char-tfidf+logistic",
  "data": {
    "classes": [
      "negative",
      "positive"
    ],
    "train_rows": 36,
    "test_rows": 12,
    "duplicates_removed": 0,
    "accuracy": 1.0
  },
  "warnings": [
    "Character n-gram baseline for labeled Arabic/multilingual text. No pretrained sentiment/medical model. Exact duplicates are removed, but author/topic/group leakage still needs domain-aware splitting."
  ]
}
```

**Terminal:** `python examples/guide/nlp_train.py` من جذر المشروع.

### 43. `nlp.topics`

Discover exploratory corpus topics using LDA

**المتطلبات:** `ml`. **المدخلات:** `data, text_column`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('nlp.topics', data=DATA/'corpus.csv', text_column='text', n_topics=2)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "sklearn.LDA",
  "data": {
    "rows": [
      {
        "topic": 0,
        "words": [
          "تجربة",
          "خدمة"
        ]
      },
      {
        "topic": 1,
        "words": [
          "رقم",
          "خدمة"
        ]
      }
    ]
  },
  "warnings": [
    "Unsupervised topics are exploratory, not known ground-truth categories. Arabic morphology/dialects require appropriate preprocessing and evaluation."
  ]
}
```

**Terminal:** `python examples/guide/nlp_topics.py` من جذر المشروع.

### 44. `nlp.similarity`

Rank text passages by lexical character TF-IDF similarity

**المتطلبات:** `ml`. **المدخلات:** `texts, query`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('nlp.similarity', texts=['تعلم بايثون','صيانة مضخة'], query='بايثون')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "sklearn.lexical-char-tfidf",
  "data": {
    "rows": [
      {
        "index": 0,
        "text": "تعلم بايثون",
        "score": 0.7745966692414835
      },
      {
        "index": 1,
        "text": "صيانة مضخة",
        "score": 0.0
      }
    ]
  },
  "warnings": [
    "Lexical similarity, NOT semantic embeddings. Use rag.search.semantic for trained semantic retrieval."
  ]
}
```

**Terminal:** `python examples/guide/nlp_similarity.py` من جذر المشروع.

### 45. `sales.forecast`

Aggregate calendar months and forecast sales using temporal baselines

**المتطلبات:** `ml`. **المدخلات:** `data`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.sales(DATA/'sales.csv', horizon=1)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "pandas.monthly-aggregation+numpy.temporal-baseline",
  "data": {
    "date_column": "date",
    "value_column": "sales",
    "history_months": 24,
    "holdout_months": 3,
    "holdout_mae": 0.0
  },
  "warnings": [
    "Forecasts are estimates, not guaranteed revenue. No calibrated uncertainty interval, promotion/exogenous or causal model. Negative forecasts are not silently clipped."
  ]
}
```

**Terminal:** `python examples/guide/sales_forecast.py` من جذر المشروع.

### 46. `data.clean`

Trim fields and remove exact duplicate CSV rows for review

**المتطلبات:** `core/system`. **المدخلات:** `data`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('data.clean', data=DATA/'appointments.csv')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.explicit-dedup",
  "data": {
    "input_rows": 3,
    "duplicates_removed": 0,
    "missing_by_column": {
      "department": 0,
      "waiting_minutes": 0
    },
    "rows": [
      {
        "department": "Lab",
        "waiting_minutes": "10"
      },
      {
        "department": "Clinic",
        "waiting_minutes": "20"
      }
    ]
  },
  "warnings": [
    "Whitespace and exact duplicates only. No arbitrary imputation or destructive in-place overwrite. Review missing-value semantics before modeling."
  ]
}
```

**Terminal:** `python examples/guide/data_clean.py` من جذر المشروع.

### 47. `data.group`

Aggregate operational records by an explicit grouping column

**المتطلبات:** `core/system`. **المدخلات:** `data, group_column`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('data.group', data=DATA/'appointments.csv', group_column='department', value_column='waiting_minutes')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.grouped-aggregation",
  "data": {
    "rows": [
      {
        "group": "Clinic",
        "count": 1,
        "total": 20.0,
        "mean": 20.0
      },
      {
        "group": "Lab",
        "count": 2,
        "total": 22.0,
        "mean": 11.0
      }
    ]
  },
  "warnings": [
    "Operational grouping only; use appropriate anonymization and authorization for patient/customer records. No clinical or credit decisions."
  ]
}
```

**Terminal:** `python examples/guide/data_group.py` من جذر المشروع.

### 48. `privacy.redact`

Mask email/phone patterns without pretending full anonymization

**المتطلبات:** `core/system`. **المدخلات:** `text`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('privacy.redact', text='Contact person@example.org +967 700 123 456')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.regex",
  "data": {
    "text": "Contact [EMAIL] [PHONE]",
    "counts": {
      "EMAIL": 1,
      "PHONE": 1
    }
  },
  "warnings": [
    "Limited email/phone masking, not comprehensive PII anonymization or HIPAA/GDPR compliance. Numbers can be false positives; names/medical identifiers may remain."
  ]
}
```

**Terminal:** `python examples/guide/privacy_redact.py` من جذر المشروع.

### 49. `finance.reconcile`

Reconcile two keyed ledgers using exact decimal amounts

**المتطلبات:** `core/system`. **المدخلات:** `left, right, key, amount_column`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('finance.reconcile', left=DATA/'left.csv', right=DATA/'right.csv', key='id', amount_column='amount')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "decimal.keyed-reconciliation",
  "data": {
    "counts": {
      "matched": 1,
      "missing-right": 1,
      "missing-left": 1
    },
    "rows": [
      {
        "key": "a",
        "status": "matched",
        "difference": "0.00"
      },
      {
        "key": "b",
        "status": "missing-right",
        "difference": null
      }
    ]
  },
  "warnings": [
    "Operational reconciliation only, not fraud detection, investment advice or automated payment approval. Currency/unit must already match."
  ]
}
```

**Terminal:** `python examples/guide/finance_reconcile.py` من جذر المشروع.

### 50. `industry.sensors`

Extract vibration/sensor statistics and explicitly sampled spectra

**المتطلبات:** `ml`. **المدخلات:** `data, columns`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('industry.sensors', data=DATA/'sensors.csv', columns=['temperature'], sample_rate=1)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "numpy.signal-features",
  "data": {
    "rows": [
      {
        "sensor": "temperature",
        "samples": 40,
        "mean": 23.425,
        "std": 9.096393516113956,
        "rms": 25.129166321229203
      }
    ]
  },
  "warnings": [
    "Frequency estimates assume uniform sampling at the explicitly supplied Hz. Features alone do not diagnose bearing faults or predict remaining useful life."
  ]
}
```

**Terminal:** `python examples/guide/industry_sensors.py` من جذر المشروع.

### 51. `industry.control`

Screen measurements against separate baseline control limits

**المتطلبات:** `core/system`. **المدخلات:** `data, column, baseline`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('industry.control', data=DATA/'sensors.csv', baseline=DATA/'baseline.csv', column='temperature')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "statistics.phase-II-shewhart",
  "data": {
    "mean": 21.975,
    "baseline_std": 0.83166499665831,
    "lower_control_limit": 19.48000501002507,
    "upper_control_limit": 24.469994989974932,
    "rows": [
      {
        "row": 0,
        "value": 21.0,
        "out_of_control": false
      },
      {
        "row": 1,
        "value": 22.0,
        "out_of_control": false
      }
    ]
  },
  "warnings": [
    "Baseline-estimated statistical control limits are NOT engineering specification limits. Check baseline stability, autocorrelation, stationarity and sampling before action."
  ]
}
```

**Terminal:** `python examples/guide/industry_control.py` من جذر المشروع.

### 52. `industry.production`

Compute production yield, rejects and optional hourly throughput

**المتطلبات:** `core/system`. **المدخلات:** `data, total_column, good_column`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('industry.production', data=DATA/'production.csv', total_column='total', good_column='good', operating_hours=3)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.production-accounting",
  "data": {
    "total_units": 300.0,
    "good_units": 285.0,
    "rejected_units": 15.0,
    "yield_fraction": 0.95,
    "reject_fraction": 0.05
  },
  "warnings": [
    "No OEE is claimed without planned time, availability, ideal cycle time and consistent definitions. Check units, duplicate shifts and count provenance."
  ]
}
```

**Terminal:** `python examples/guide/industry_production.py` من جذر المشروع.

### 53. `industry.maintenance`

Evaluate a supervised maintenance-label classifier on historical data

**المتطلبات:** `ml`. **المدخلات:** `data, target`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('industry.maintenance', data=DATA/'numeric.csv', target='target')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "scikit-learn.RandomForest",
  "data": {
    "problem": "classification",
    "target": "target",
    "features": [
      "x",
      "y"
    ],
    "numeric_features": [
      "x",
      "y"
    ],
    "train_rows": 75
  },
  "warnings": [
    "Held-out split, not cross-validation. Not suitable evidence for time-series, grouped or causal claims; use domain-specific splits in future versions.",
    "Supervised historical-label classifier, not calibrated failure probability or remaining useful life. Random split is a teaching baseline; asset/time grouped validation is required before production maintenance decisions. No automatic shutdown or actuation."
  ]
}
```

**Terminal:** `python examples/guide/industry_maintenance.py` من جذر المشروع.

### 54. `industry.defects`

Locate aligned-reference image differences for quality screening

**المتطلبات:** `vision`. **المدخلات:** `image, reference`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
media_fixtures(DATA, PHOTO)
result = ai.inspect(DATA/'bad.png', reference=DATA/'good.png', output=OUT/'difference.png')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "opencv.aligned-reference-difference",
  "data": {
    "candidate_count": 1,
    "changed_fraction": 0.05865478515625,
    "rows": [
      {
        "x": 35,
        "y": 45,
        "width": 31,
        "height": 31
      }
    ],
    "mask_path": "/tmp/tmpmz8qvmm3/outputs/difference.png"
  },
  "warnings": [
    "Difference candidates, NOT a semantic defect diagnosis or validated factory acceptance rule. Lighting, pose and alignment changes can cause false alarms. Requires a representative known-good reference."
  ]
}
```

**Terminal:** `python examples/guide/industry_defects.py` من جذر المشروع.

### 55. `database.profile`

Read SQLite schema and row counts without modifying the database

**المتطلبات:** `core/system`. **المدخلات:** `database`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('database.profile', database=DATA/'factory.sqlite')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "sqlite.read-only",
  "data": {
    "rows": [
      {
        "table": "readings",
        "row_count": 1,
        "columns": [
          {
            "name": "id",
            "type": "INTEGER",
            "not_null": false,
            "primary_key_position": 1
          },
          {
            "name": "value",
            "type": "REAL",
            "not_null": false,
            "primary_key_position": 0
          }
        ]
      }
    ]
  },
  "warnings": [
    "Schema and row counts only; no row values disclosed, SQL repairs, writes or remote DB access. This is not a vulnerability audit."
  ]
}
```

**Terminal:** `python examples/guide/database_profile.py` من جذر المشروع.

### 56. `code.tests.generate`

Generate untrusted unittest suggestions with syntax diagnostics

**المتطلبات:** `local`. **المدخلات:** `code`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('code.tests.generate', code='def add(a,b):\n    return a+b\n', max_new_tokens=80)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "transformers.local-causal-lm",
  "data": {
    "text": "```python\ndef add(a,b):\n    return a+b\n```\n\nThis function takes two arguments `a` and `b`, adds them together, and returns the result. It does not execute the function.",
    "generated_tokens": 48,
    "input_tokens": 58,
    "syntax_valid": true
  },
  "warnings": [
    "Generated content can be wrong. Default 135M model is English-first and limited; not a strongest-model or Arabic-quality claim. Input is truncated to 1024 tokens.",
    "LLM-generated test suggestions, not validated test coverage or guaranteed assertions. Never execute untrusted suggestions automatically."
  ]
}
```

**Terminal:** `python examples/guide/code_tests_generate.py` من جذر المشروع.

### 57. `api.schema`

Build the authenticated text API OpenAPI schema

**المتطلبات:** `api`. **المدخلات:** `راجع الوظيفة`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('api.schema')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "fastapi.openapi",
  "data": {
    "openapi": {
      "openapi": "3.1.0",
      "info": {
        "title": "AlFarouq AI",
        "description": "Authenticated local text services; not a clinical/financial decision system.",
        "version": "0.3.0a1"
      },
      "paths": {
        "/health": {
          "get": {
            "summary": "Health",
            "operationId": "health_health_get",
            "responses": {
              "200": {
                "description": "Successful Response",
                "content": {
                  "application/json": {
                    "schema": {}
                  }
                }
              }
            }
          }
        },
        "/v1/run": {
          "post": {
            "summary": "Run",
            "operationId": "run_v1_run_post",
            "responses": {
              "200": {
                "description": "Successful Response",
                "content": {
                  "application/json": {
                    "schema": {}
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "warnings": [
    "TestClient/schema validation is not public deployment, TLS, rate limiting or a production security audit."
  ]
}
```

**Terminal:** `python examples/guide/api_schema.py` من جذر المشروع.

### 58. `onnx.predict`

Run reviewed local ONNX tensors with the CPU runtime

**المتطلبات:** `onnx`. **المدخلات:** `model_path, inputs`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
create_onnx(DATA/'double.onnx')
result = ai.run('onnx.predict', model_path=DATA/'double.onnx', inputs={'x':[[2.],[3.]]})
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "onnxruntime.CPUExecutionProvider",
  "data": {
    "outputs": {
      "y": [
        [
          4.0
        ],
        [
          6.0
        ]
      ]
    }
  },
  "warnings": [
    "Only reviewed local models; native runtime is not an OS sandbox. External tensor data and custom-op libraries are not loaded by this adapter."
  ]
}
```

**Terminal:** `python examples/guide/onnx_predict.py` من جذر المشروع.

### 59. `tensorflow.predict`

Run a reviewed local single-output Keras model

**المتطلبات:** `tensorflow`. **المدخلات:** `model_path, inputs`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
import tensorflow as tf
model=tf.keras.Sequential([tf.keras.layers.Input(shape=(1,)),tf.keras.layers.Dense(1)])
import numpy as np
model.layers[0].set_weights([np.array([[2.]],dtype='float32'),np.array([1.],dtype='float32')])
model.save(DATA/'linear.keras')
result = ai.run('tensorflow.predict', model_path=DATA/'linear.keras', inputs=[[2.]])
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "tensorflow.keras.cpu",
  "data": {
    "outputs": [
      [
        5.0
      ]
    ]
  },
  "warnings": [
    "safe_mode is defense in depth, not permission to load hostile files. Reviewed models only; no custom objects or training API claimed."
  ]
}
```

**Terminal:** `python examples/guide/tensorflow_predict.py` من جذر المشروع.

### 60. `llm.compatible`

Call an explicitly approved OpenAI-compatible optional inference endpoint

**المتطلبات:** `core/system`. **المدخلات:** `prompt, endpoint, model`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
with model_server() as origin:
    result = Client(Config(allow_network=True)).run('llm.compatible', prompt='What is the capital of France?', endpoint=origin+'/v1', model='reference-smollm')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "openai-compatible-http",
  "data": {
    "text": "The capital of France is Paris.",
    "model": "reference-smollm"
  },
  "warnings": [
    "Protocol compatible with vLLM-like endpoints; no claim that a particular third-party server or cloud model was deployed/tested. Provider terms/costs remain user responsibility."
  ]
}
```

**Terminal:** `python examples/guide/llm_compatible.py` من جذر المشروع.

### 61. `iot.modbus.read`

Read bounded holding registers from an approved local gateway

**المتطلبات:** `industrial`. **المدخلات:** `host, address, count`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
with modbus_server() as port:
    result = Client(Config(allow_network=True)).run('iot.modbus.read', host='127.0.0.1', port=port, address=0, count=2)
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "pymodbus.tcp-read-only",
  "data": {
    "address": 0,
    "device_id": 1,
    "registers": [
      10,
      20
    ],
    "rows": [
      {
        "address": 0,
        "raw_uint16": 10
      },
      {
        "address": 1,
        "raw_uint16": 20
      }
    ]
  },
  "warnings": [
    "Raw 16-bit registers; scaling, signedness, byte order and engineering units are device-specific. Local server verification is not physical PLC validation."
  ]
}
```

**Terminal:** `python examples/guide/iot_modbus_read.py` من جذر المشروع.

### 62. `document.insights`

Extract text, keywords, dates and an extractive summary from a file

**المتطلبات:** `documents`. **المدخلات:** `document`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = AI('حلل هذا الملف واستخرج أهم المعلومات', file=DATA/'note.txt')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.text+extractive-statistics",
  "data": {
    "characters": 117,
    "words": 18,
    "summary": "AlFarouq AI helps students use Python. Temperature sensors measure heat. خالد سلمان مؤسس المشروع.",
    "keywords": [
      [
        "alfarouq",
        1
      ],
      [
        "ai",
        1
      ]
    ],
    "dates_found": [
      "2026-11-16"
    ]
  },
  "warnings": [
    "Text extraction only; scanned PDFs need OCR, formulas are not recalculated, complex layout may be lost.",
    "Extractive information only, not legal/clinical interpretation or automatic scanned-PDF OCR."
  ]
}
```

**Terminal:** `python examples/guide/document_insights.py` من جذر المشروع.

### 63. `document.search`

Search document passages lexically with source references

**المتطلبات:** `documents`. **المدخلات:** `document, query`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = ai.run('document.search', document=DATA/'note.txt', query='Python')
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.lexical-tfidf-cosine",
  "data": {
    "query": "Python",
    "rows": [
      {
        "id": 0,
        "source": "/tmp/tmp55yahpq5/data/note.txt",
        "start": 0,
        "end": 117,
        "text": "AlFarouq AI helps students use Python. Temperature sensors measure heat.\nخالد سلمان مؤسس المشروع. التاريخ 2026-11-16."
      }
    ]
  },
  "warnings": [
    "Lexical retrieval, not semantic embeddings. No generated answer was fabricated."
  ]
}
```

**Terminal:** `python examples/guide/document_search.py` من جذر المشروع.

### 64. `ai.search`

Solve a bounded unit-cost grid shortest path with A-star

**المتطلبات:** `core/system`. **المدخلات:** `grid, start, goal`.

**نص نُفّذ بنجاح** بعد التهيئة المشتركة:

```python
result = AI('astar', grid=[[0,0,0],[0,1,0]], start=[0,0], goal=[1,2])
print(result.to_dict())
```

**مقتطف ناتج فعلي للعينة، لا وعد بتطابق النص أو المسارات:**

```json
{
  "backend": "stdlib.A-star-Manhattan",
  "data": {
    "found": true,
    "cost": 3,
    "path": [
      [
        0,
        0
      ],
      [
        0,
        1
      ]
    ],
    "expanded": 5,
    "rows": [
      {
        "step": 0,
        "row": 0,
        "column": 0
      },
      {
        "step": 1,
        "row": 0,
        "column": 1
      }
    ]
  },
  "warnings": [
    "Four-neighbor unit-cost grid exercise, not autonomous navigation or robot safety."
  ]
}
```

**Terminal:** `python examples/guide/ai_search.py` من جذر المشروع.


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
