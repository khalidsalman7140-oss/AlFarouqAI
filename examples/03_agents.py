"""Real document -> summarizer data flow with a bounded DAG."""
from pathlib import Path
from alfarouqai import AgentTeam, Step, Ref
root = Path(__file__).resolve().parents[1]
result = AgentTeam(workers=2).run([
    Step('read', 'document.read', {'document': root/'examples/data/knowledge.txt'}, agent='document-specialist'),
    Step('summarize', 'text.analyze', {'text': Ref('read','text')}, agent='text-specialist'),
    Step('review_code', 'code.analyze', {'code':'def square(x):\n    return x*x\n'}, agent='code-reviewer'),
])
print(result.to_dict())
