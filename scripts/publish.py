"""Owner-operated GitHub publication helper. Dry-run unless explicitly approved.
No tokens are read from source, printed, embedded or sent to this assistant.
"""
from pathlib import Path
import argparse,json,re,shutil,subprocess,tempfile,sys
ROOT=Path(__file__).resolve().parents[1]

def command(args,cwd=None):return subprocess.run(args,cwd=cwd,check=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',required=True,help='Your authorized OWNER/REPOSITORY');p.add_argument('--public',action='store_true');p.add_argument('--approve-publication',action='store_true');args=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',args.repo):p.error('Use a valid OWNER/REPOSITORY')
    plan={'repository':args.repo,'visibility':'public' if args.public else 'private','requires':['git','GitHub CLI','owner gh auth login','review LICENSE/identity/secret scan'],'public_upload_now':args.approve_publication}
    print(json.dumps(plan,indent=2))
    if not args.approve_publication:return
    if not shutil.which('gh') or not shutil.which('git'):raise SystemExit('Install git and GitHub CLI first; no publication occurred.')
    if subprocess.run(['gh','auth','status'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:raise SystemExit('GitHub is not authenticated. Run gh auth login yourself, then repeat. No publication occurred.')
    # New repository only: never overwrite/push into a pre-existing remote silently.
    if subprocess.run(['gh','repo','view',args.repo],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:raise SystemExit('Repository already exists. Use normal git review/push, not this new-repository helper.')
    command([sys.executable,str(ROOT/'scripts/prepublish_check.py')])
    with tempfile.TemporaryDirectory(prefix='alfarouq-publish-') as tmp:
        staging=Path(tmp)/'project'
        ignored={'ALFAROUQ_AI_OWNER_MASTER_GUIDE_AR.md','ALFAROUQ_AI_OWNER_MASTER_GUIDE_AR.html','.git','.venv','venv','__pycache__','.pytest_cache','build','dist','demo-output','history','.env','.env.local','token.json','credentials.json','ALFAROUQAI_FULL_REPORT.txt'}
        def ignore(path,names):return [n for n in names if n in ignored or n.endswith(('.pyc','.private.log','.pem','.key')) or n.startswith('credentials')]
        shutil.copytree(ROOT,staging,ignore=ignore)
        command(['git','init','-b','main'],cwd=staging)
        command(['git','add','.'],cwd=staging)
        command(['git','-c','user.name=Khalid Salman','-c','user.email=khalidsalman7140@gmail.com','commit','-m','Release AlFarouq AI 0.3.0a1'],cwd=staging)
        command(['gh','repo','create',args.repo,'--public' if args.public else '--private','--source',str(staging),'--remote','origin','--push'],cwd=staging)
    print('Published repository: https://github.com/'+args.repo)
if __name__=='__main__':main()
