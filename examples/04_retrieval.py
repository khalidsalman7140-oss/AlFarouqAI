from pathlib import Path
from alfarouqai import KnowledgeBase
root = Path(__file__).resolve().parents[1]
kb = KnowledgeBase(chunk_size=140, overlap=20)
kb.add((root/'examples/data/knowledge.txt').read_text(), source='knowledge.txt')
print(kb.search('خالد سلمان').to_dict())
print(kb.search('runtime dependencies').to_dict())
# SemanticIndex('/path/to/reviewed/local/embedding-model') is optional and different.
