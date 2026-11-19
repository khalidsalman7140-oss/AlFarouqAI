"""Assemble an organized ZIP, verify CRC and extracted hashes. No publication.

Run after tests, capture_examples.py, build_docs.py and python -m build.
Output is alongside the project folder; the original folder is retained.
"""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile
from validate_project import validate

ROOT=Path(__file__).resolve().parents[1]

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda:f.read(65536),b''):h.update(data)
    return h.hexdigest()

def main():
    # Only known build/cache outputs; never delete source, docs, assets or reports.
    for path in list(ROOT.rglob('__pycache__'))+list(ROOT.rglob('*.egg-info')):
        if path.is_dir():shutil.rmtree(path)
    for name in ('.pytest_cache','build'):
        path=ROOT/name
        if path.is_dir():shutil.rmtree(path)
    status=validate(ROOT)
    (ROOT/'archive-validation.json').write_text(json.dumps({'scope':'project structure and offline links checked before archive; CRC/extracted hashes checked by package_delivery.py and validate_project.py','checks':status,'zip_crc_required':True,'extracted_sha256_required':True},indent=2),encoding='utf-8')
    files=[]
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path.name=='DELIVERY_MANIFEST.json':continue
        if any(part in {'.git','.venv','__pycache__','.pytest_cache','build'} for part in path.relative_to(ROOT).parts):continue
        files.append({'path':path.relative_to(ROOT).as_posix(),'bytes':path.stat().st_size,'sha256':sha(path)})
    (ROOT/'DELIVERY_MANIFEST.json').write_text(json.dumps({'algorithm':'sha256','scope':'every delivered file except this manifest itself','files':files},ensure_ascii=False,indent=2),encoding='utf-8')
    archive=ROOT.parent/'AlFarouqAI-0.3.0a1.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for item in files:z.write(ROOT/item['path'],'AlFarouqAI/'+item['path'])
        z.write(ROOT/'DELIVERY_MANIFEST.json','AlFarouqAI/DELIVERY_MANIFEST.json')
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for item in files:
            assert hashlib.sha256(z.read('AlFarouqAI/'+item['path'])).hexdigest()==item['sha256']
    receipt={'archive':archive.name,'bytes':archive.stat().st_size,'files':len(files)+1,'sha256':sha(archive),'crc_ok':True,'all_file_hashes_ok':True}
    (archive.parent/(archive.name+'.sha256')).write_text(receipt['sha256']+'  '+archive.name+'\n',encoding='utf-8')
    (archive.parent/'verification-receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
