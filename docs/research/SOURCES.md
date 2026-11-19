# Research evidence and decisions | مصادر البحث والقرارات
Research date: 2026-11-14. The following pages were retrieved during this task.
This is targeted architecture/license research, not an exhaustive security or legal audit.

| Source | Finding used | Engineering consequence |
|---|---|---|
| [PyPA pyproject guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) | standard optional-dependencies, build-system and entry points | dependency-free core with extras; setuptools build backend |
| [PyPA plugin guide](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#plugin-entry-points) | importlib.metadata discovers plugins; load() imports a module | opt-in plugin execution, not implicit trust |
| [scikit-learn persistence](https://scikit-learn.org/stable/model_persistence.html) | pickle/joblib loading can execute code; matching package versions matter; skops and ONNX have their own caveats | no unsafe pickle load; save-only optional skops; record versions |
| [scikit-learn PyPI](https://pypi.org/project/scikit-learn/) | BSD-3-Clause; latest retrieved version needs Python >=3.11 | constrain library range; Python 3.10 resolves older compatible wheels, not always newest |
| [Ollama API](https://docs.ollama.com/api/introduction) | local origin localhost:11434 and /api/chat; cloud and local differ | explicit local model, local-first endpoint, no mandatory key |
| [Open Source Definition](https://opensource.org/osd) | free redistribution and derived works are requirements | no-copy/no-reuse license cannot be called OSI open source |
| [Ultralytics license](https://www.ultralytics.com/license) | vendor presents AGPL and enterprise terms | do not silently include it in restrictive original-work distribution; review exact integration before adoption |
| [OpenCV license](https://opencv.org/license/) | 4.5+ Apache-2.0; older versions BSD | use modern optional OpenCV; check wheel/native notices |
| [Transformers license](https://github.com/huggingface/transformers/blob/main/LICENSE) | license source retrieved; weights remain separate | optional local model adapter, no assumption of weight-use rights |
| [HF repository licenses](https://huggingface.co/docs/hub/en/repositories-licenses) | many incompatible model licenses exist | review every exact model repository/version, not just its framework |
| [SentenceTransformers](https://github.com/huggingface/sentence-transformers) | local embedding support and license link | optional semantic adapter; lexical index honestly labeled |
| [SentenceTransformers license](https://github.com/huggingface/sentence-transformers/blob/main/LICENSE) | license file retrieved; linked official announcement states Apache-2.0 | separate library/weight review |
| [Official SentenceTransformers announcement](https://huggingface.co/blog/sentence-transformers-joins-hf) | search result states Apache-2.0 | Apache family is an initial library license classification, not model clearance |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | CPU/int8 and local CTranslate2 directory support | optional local speech adapter |
| [faster-whisper license](https://github.com/SYSTRAN/faster-whisper/blob/master/LICENSE) | MIT indicated by retrieved search listing; full GitHub crawl did not expose text | preliminary license classification; exact deployed revision should be re-reviewed |
| [pypdf PyPI](https://pypi.org/project/pypdf/) | text extraction, release info; crawler did not expose exact license | inspect actual installed distribution license metadata and notices |
| [python-docx PyPI](https://pypi.org/project/python-docx/) | DOCX support, release metadata | adapter and local fixture; inspect installed license metadata |
| [openpyxl PyPI](https://pypi.org/project/openpyxl/) | XLSX support and parser caveats | cached-value extraction, no recalculation; inspect installed license metadata |
| [pandas PyPI](https://pypi.org/project/pandas/) | BSD-3-Clause | optional tabular preprocessing; preserve notices |
| [ONNX license](https://github.com/onnx/onnx/blob/main/LICENSE) | license source retrieved, not an implemented engine | future portability candidate only; no ONNX capability claim |

## Independent synthesis | الخلاصة المستقلة
The best starting point is a facade with honest typed contracts and lazy adapters,
not a promise that any natural-language request can safely run arbitrary tools.
A framework's permissive license does not grant rights to model weights, datasets,
codecs, trademarks, or another author's work. No model weights or external library
sources are vendored here. Legal review before distribution/commercial deployment
remains necessary, especially for restrictive founder terms and copyleft tools.

Observed compatibility evidence: OpenCV 5.0 in the initial host lacked
CascadeClassifier. A clean environment with OpenCV 4.12 fixed the actual integration,
and the declared vision range was tightened to >=4.10,<5. No quality claim is based
only on an import succeeding. Model inference not executed is explicitly marked.
