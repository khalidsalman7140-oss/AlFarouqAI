"""Execute exact guide snippets in fresh workers before labeling them verified."""
from pathlib import Path
import argparse,json,os,subprocess,sys,time,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from examples.guide_catalog import CASES,UNVERIFIED,COMMON

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case');parser.add_argument('--installed',action='store_true');args=parser.parse_args()
    if args.case:
        namespace={};exec(compile(COMMON+'\n'+CASES[args.case],'<guide:'+args.case+'>','exec'),namespace)
        result=namespace['result'];obj=result.to_dict();json.dumps(obj,allow_nan=False)
        if result.task!=args.case:raise AssertionError((args.case,result.task))
        target=ROOT/'reports/coding-guide-results';target.mkdir(parents=True,exist_ok=True)
        (target/(args.case+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
        assets=ROOT/'reports/coding-guide-assets'/args.case
        if any(namespace['OUT'].iterdir()):shutil.copytree(namespace['OUT'],assets,dirs_exist_ok=True)
        namespace['workspace'].cleanup();return
    target=ROOT/'reports/coding-guide-results';target.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env.update(USE_TF='0',TF_CPP_MIN_LOG_LEVEL='2',OMP_NUM_THREADS='2')
    if args.installed:env.pop('PYTHONPATH',None)
    else:env['PYTHONPATH']=str(ROOT/'src')
    records=[]
    for task in CASES:
        start=time.perf_counter();log=target/(task+'.log')
        with log.open('w') as stream:
            try:code=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--case',task],cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=180).returncode
            except subprocess.TimeoutExpired:code=-999
        records.append({'task':task,'passed':code==0,'returncode':code,'elapsed_seconds':round(time.perf_counter()-start,3),'log':str(log.relative_to(ROOT)),'snippet_sha256':hashlib.sha256((COMMON+'\n'+CASES[task]).encode()).hexdigest()})
        (ROOT/'reports/coding-guide-verification.json').write_text(json.dumps({'installed_wheel':args.installed,'examples':records,'untested':UNVERIFIED},ensure_ascii=False,indent=2))
        print(task,code,flush=True)
        if code:raise SystemExit('Example failed; do not label verified: '+task)
    print('Every executable guide example passed:',len(records),flush=True)
if __name__=='__main__':main()
