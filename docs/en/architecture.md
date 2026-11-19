> Preserved 0.1.0 documentation. Current status: [0.2 handbook](handbook-0.2.md) and [0.2 matrix](capabilities-0.2.md).

# Architecture and independent engineering decisions
[العربية](../ar/architecture.md) · [Research sources](../research/SOURCES.md)

```text
Python / CLI / VS Code
       |
AI conservative router ---- Client.run(explicit_task)
       +-------------------+
                           |
              Registry + Capability contracts
                           |
              Config / validation / consent policy
                           |
    stdlib tools | lazy optional engines | opt-in Ollama
                           |
           Result + warnings + backend provenance
                           |
                 JSON CSV MD HTML TXT

AgentTeam: validate DAG -> specialist levels -> Ref data flow -> schema reviewer
```

The goal is a stable facade, not rewriting every external engine or hiding material
choices. Optional dependencies and plugin entry points follow Python packaging
standards. Every capability declares inputs and returns an auditable Result.
A conservative router is cheaper, lighter and easier to test than making an LLM
mandatory; unrestricted natural-language planning is deliberately not claimed.

| Concern | Alternatives considered | Decision |
|---|---|---|
| Packaging | monolith; auto-install on import; extras | dependency-free core + explicit extras + consent-only dedicated venv installer |
| Planning | mandatory agent framework/LLM; rules | explainable bilingual rules now; schema-constrained LLM planner later |
| Agents | opaque autonomy; bounded graph | real DAG execution, budget/allowlist, specialist tools and schema review |
| Tabular ML | custom algorithms; established pipelines | scikit-learn pipelines, explicit target/problem, split before preprocessing |
| Persistence | pickle/joblib; skops; ONNX | optional skops save only; no untrusted load; ONNX later |
| Vision | YOLO default; OpenCV; Transformers | OpenCV 4.x for tested face/motion; separate local detection adapter; no default AGPL integration |
| Search | mandatory vector DB; lexical index; embeddings | core JSON/TF-IDF; optional local SentenceTransformers |
| LLM | mandatory cloud API; local server | explicit model + Ollama opt-in, no paid service required |
| Licensing | call restrictive code open source; reserve rights | current original source Apache-2.0, founder assets separately reserved |

Security is a policy boundary, not process isolation. No runtime installation,
no generated-code execution, no auto plugin import, no default network and no model
weights in the release. Hostile files/plugins still need OS-level isolation.

Before production: process resource limits, task cancellation/timeouts, async,
platform hash-locks, Arabic benchmark suites, data/privacy controls, telemetry
that is off by default, experiment/model provenance, domain-aware splits, model
license manifests, security review and robust parser fuzzing. Compare local model
quality/latency/RAM/license on a defined benchmark; no strongest-model comparison
was performed during this delivery. See linked sources for evidence, not claims
that one library license also licenses its model weights.
