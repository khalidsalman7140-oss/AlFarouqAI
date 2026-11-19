"""Run release tests in isolated sequential workers for small-RAM machines.

Requires prepared model caches and optional/system engines. No publication.
Example: ALFAROUQ_MODEL_HOME=/path python scripts/run_verification.py
Use --installed after installing the release wheel to disable src path injection.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--installed',action='store_true');args=parser.parse_args()
    env=os.environ.copy();env['ALFAROUQ_RUN_MODELS']='1';env['USE_TF']='0';env['TF_CPP_MIN_LOG_LEVEL']='2'
    if args.installed:env.pop('PYTHONPATH',None)
    else:env['PYTHONPATH']=str(ROOT/'src')
    output=ROOT/'reports/verification-workers-0.3';output.mkdir(parents=True,exist_ok=True)
    base=[sys.executable,'-m','pytest','-q']
    if args.installed:base+=['-o','pythonpath=']
    collect=subprocess.run(base+['--collect-only','-m','model'],cwd=ROOT,env=env,capture_output=True,text=True,check=True)
    cases=[line.strip() for line in collect.stdout.splitlines() if line.strip().startswith('tests/') and '::' in line]
    jobs=[['-m','not model']]+[[case] for case in cases]
    aggregate=ET.Element('testsuites');totals={'tests':0,'failures':0,'errors':0,'skipped':0};runs=[]
    for i,job in enumerate(jobs):
        xml=output/f'worker-{i}.xml';log=output/f'worker-{i}.log'
        with log.open('w') as stream:
            proc=subprocess.run(base+job+['--junitxml='+str(xml)],cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=240)
        print(f'worker {i}: exit {proc.returncode} — {job}',flush=True)
        if not xml.exists():raise SystemExit('Worker did not produce results; inspect '+str(log))
        suites=ET.parse(xml).getroot()
        for suite in suites.iter('testsuite'):
            aggregate.append(suite)
            for key in totals:totals[key]+=int(suite.attrib.get(key,0))
        runs.append({'job':job,'returncode':proc.returncode,'log':str(log.relative_to(ROOT))})
        if proc.returncode:raise SystemExit('Verification failed; inspect '+str(log))
    for k,v in totals.items():aggregate.set(k,str(v))
    ET.ElementTree(aggregate).write(ROOT/'reports/pytest-0.3.xml',encoding='utf-8',xml_declaration=True)
    record={'version':'0.3.0a1','execution':'sequential isolated pytest workers; not a monolithic same-process run','installed_wheel':args.installed,'counts':totals,'workers':runs,'actual_model_tests_opted_in':True}
    (ROOT/'reports/verification-run-0.3.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(json.dumps(record,indent=2))

if __name__=='__main__':main()
