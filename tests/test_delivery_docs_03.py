"""Documentation/release invariants; no network or optional engines required."""
import ast
import json
from pathlib import Path
from alfarouqai import Client
ROOT=Path(__file__).resolve().parents[1]

def test_complete_reference_covers_every_registered_capability():
    content=(ROOT/'ALFAROUQ_AI_COMPLETE_CODING_GUIDE.md').read_text()
    for cap in Client().capabilities():assert '`'+cap['name']+'`' in content
    for name in ('USER_GUIDE_AR.md','USER_GUIDE_EN.md'):
        assert (ROOT/name).stat().st_size>15000
    owner=ROOT/'ALFAROUQ_AI_OWNER_MASTER_GUIDE_AR.md'
    if owner.exists():assert owner.stat().st_size>15000  # Intentionally absent from public distributions.


def test_standalone_guide_examples_are_real_compilable_files():
    # The integration executor separately executes these same COMMON+CASES bodies.
    paths=list((ROOT/'examples/guide').glob('*.py'))
    assert len(paths)==61
    for p in paths:ast.parse(p.read_text(),filename=p.name)
    evidence=ROOT/'reports/coding-guide-verification.json'
    if evidence.exists():
        record=json.loads(evidence.read_text())
        assert len(record['examples'])==61 and all(x['passed'] for x in record['examples'])


def test_internal_owner_guide_not_in_public_staging_or_sdist():
    tree=ast.parse((ROOT/'scripts/publish.py').read_text());ignored=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ignored' for t in n.targets):ignored=ast.literal_eval(n.value)
    assert 'ALFAROUQ_AI_OWNER_MASTER_GUIDE_AR.md' in ignored
    assert 'exclude ALFAROUQ_AI_OWNER_MASTER_GUIDE_AR.md' in (ROOT/'MANIFEST.in').read_text()
