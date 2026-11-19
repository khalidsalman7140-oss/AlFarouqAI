"""Static release gate. Not a security audit and never uploads anything."""
from pathlib import Path
import ast,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
IGNORED={'.git','.venv','venv','__pycache__','.pytest_cache','build','history'}

def main():
    problems=[];scanned=0
    patterns=[re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}'),re.compile(r'github_pat_[A-Za-z0-9_]{30,}'),re.compile(r'AIza[0-9A-Za-z_-]{30,}'),re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]
    for p in ROOT.rglob('*'):
        if not p.is_file() or any(x in IGNORED for x in p.relative_to(ROOT).parts) or p.suffix in ('.zip','.gz','.whl','.png','.jpg','.wav','.safetensors','.onnx','.keras'):continue
        if p.name in ('credentials.json','token.json','.env') or p.name.startswith('credentials-'):problems.append({'file':str(p.relative_to(ROOT)),'issue':'credential file must not be released'});continue
        if p.stat().st_size>2_000_000:continue
        text=p.read_text(encoding='utf-8',errors='ignore');scanned+=1
        if any(pattern.search(text) for pattern in patterns):problems.append({'file':str(p.relative_to(ROOT)),'issue':'potential secret value detected (redacted)'})
        if p.suffix=='.py':
            try:ast.parse(text)
            except SyntaxError as exc:problems.append({'file':str(p.relative_to(ROOT)),'issue':'syntax error','line':exc.lineno})
    metadata=(ROOT/'pyproject.toml').read_text()
    version=re.search(r'^version = "([^"]+)"',metadata,re.M).group(1)
    core=ast.parse((ROOT/'src/alfarouqai/core.py').read_text())
    core_version=next(n.value.value for n in core.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='__version__' for t in n.targets))
    if version!=core_version:problems.append({'issue':'metadata/core version mismatch'})
    if 'license = "Apache-2.0"' not in metadata or 'Apache License' not in (ROOT/'LICENSE').read_text():problems.append({'issue':'current Apache license is not correctly installed'})
    record={'version':version,'scanned_text_files':scanned,'issues':problems,'scope':'static high-confidence secret patterns, syntax, version and license checks; not a complete audit'}
    print(json.dumps(record,indent=2));return bool(problems)
if __name__=='__main__':raise SystemExit(main())
