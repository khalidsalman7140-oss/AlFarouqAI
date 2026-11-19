"""Offline structural/link/archive verification. Does not publish anything."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse
import hashlib
import json
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self): super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v:self.links.append(v)

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda:f.read(65536),b''):h.update(data)
    return h.hexdigest()

def validate(root):
    required=['pyproject.toml','LICENSE','NOTICE','README.md','README.ar.md','docs/index.html','docs/ar/guide.html','docs/en/guide.html','identity/founder/khalid-salman-original.jpg','tests/test_core.py','tests/test_optional.py','tests/test_transport.py','reports/pytest.xml','reports/wheel-smoke.json','reports/FINAL_REPORT.ar.md','reports/FINAL_REPORT.en.md','dist/alfarouqai-0.3.0a1-py3-none-any.whl','dist/alfarouqai-0.3.0a1.tar.gz']
    missing=[name for name in required if not (root/name).is_file()]
    if missing:raise AssertionError({'missing':missing})
    broken=[];checked=0
    for path in root.rglob('*.html'):
        parser=Links();parser.feed(path.read_text(encoding='utf-8'))
        for link in parser.links:
            parsed=urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:continue
            target=(path.parent/unquote(parsed.path)).resolve()
            checked+=1
            if not target.exists():broken.append({'page':str(path.relative_to(root)),'target':link})
    if broken:raise AssertionError({'broken_links':broken})
    wheel=root/'dist/alfarouqai-0.3.0a1-py3-none-any.whl'
    with zipfile.ZipFile(wheel) as z:
        assert z.testzip() is None
        assert 'alfarouqai/__init__.py' in z.namelist()
    return {'required_paths':len(required),'local_html_links_checked':checked,'broken_links':0,'founder_photo_sha256':digest(root/'identity/founder/khalid-salman-original.jpg'),'wheel_crc_ok':True}

def main():
    p=argparse.ArgumentParser();p.add_argument('--archive');args=p.parse_args()
    report=validate(ROOT)
    if args.archive:
        archive=Path(args.archive)
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            names=z.namelist()
            assert len(names)==len(set(names))
            assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names)
            assert all(n.startswith('AlFarouqAI/') for n in names)
            with tempfile.TemporaryDirectory() as temp:
                z.extractall(temp)
                extracted=Path(temp)/'AlFarouqAI'
                validate(extracted)
                manifest=json.loads((extracted/'DELIVERY_MANIFEST.json').read_text())
                for item in manifest['files']:
                    assert digest(extracted/item['path'])==item['sha256'],item['path']
        report.update({'zip_crc_ok':True,'extract_and_file_hashes_ok':True,'zip_entries':len(names),'zip_sha256':digest(archive),'zip_bytes':archive.stat().st_size})
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
