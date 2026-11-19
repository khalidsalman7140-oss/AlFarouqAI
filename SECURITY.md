# 0.2 security addendum
The original policy below remains applicable. New risk boundaries:
- Model cache downloads require explicit network/model approval; hashes record bytes, not publisher authentication. Review local model files and pinned revisions.
- Local TorchVision uses official hash-prefix checked weights and weights_only=True; keep PyTorch patched. Neural persistence uses safetensors+validated JSON.
- code.test executes TRUSTED code with OS privileges; -I and timeout are NOT a sandbox.
- Serial and MQTT publish can actuate devices; separate explicit consent, no autonomous default access.
- SQLite/FAISS are bounded local persistence, not hostile-file/process isolation. RAG cannot guarantee factual entailment.
- Diffusion adapters are unverified actual-weight paths; do not use for production or unreviewed private inputs.

# Security policy | سياسة الأمان
Report privately to khalidsalman7140@gmail.com; do not post secrets publicly.
This alpha has not received an independent penetration test or security audit.
Core defaults: no network, no model downloads, no shell execution, no automatic
plugin loading, no untrusted pickle loading, bounded files and agent steps.
Network consent includes localhost. Remote endpoints also need allow_remote
and HTTPS. Redirects and environment proxies are disabled for Ollama transport.
A local server can still expose a cloud-backed model alias: configure Ollama
locally and independently verify it; the library cannot prove server behavior.
Plugins run full Python privileges after consent, NOT inside an OS sandbox.
pip installation may execute third-party build code; use disposable owned venvs.
Native media/PDF parsers can have vulnerabilities. Byte/pixel limits are not a
memory sandbox or a decompression-bomb guarantee; parse hostile files in a
separately resource-limited process/container. Never feed private files to an
untrusted provider. AST and log findings are heuristics, not security assurance.
RAG excerpts are untrusted input; cite sources and never turn them into tools.
CSV export prefixes formula-looking strings. Reports escape HTML output.
تعزل النسخة الحالية السياسات منطقياً، ولا توفر عزلاً أمنياً على مستوى نظام التشغيل.
