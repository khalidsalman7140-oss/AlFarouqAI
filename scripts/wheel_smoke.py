"""Run with an installed wheel from outside the checkout; writes evidence only."""
import argparse
import importlib.metadata
import json
import sys
import tempfile
from pathlib import Path
from alfarouqai import AI, Client, AgentTeam, Step, Ref, KnowledgeBase


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True); args=parser.parse_args()
    dist=importlib.metadata.distribution('alfarouqai')
    requirements=dist.metadata.get_all('Requires-Dist',[])
    mandatory=[r for r in requirements if 'extra ==' not in r and 'extra==' not in r]
    assert mandatory==[],mandatory
    result=AI('analyze this text',text='Local tools help students. Python enables research.')
    assert result.data['words']==7
    kb=KnowledgeBase();kb.add('Khalid Salman founded AlFarouq AI.',source='fixture')
    assert kb.search('Khalid').data['rows'][0]['source']=='fixture'
    with tempfile.TemporaryDirectory() as tmp:
        csv_path=Path(tmp)/'sample.csv'; csv_path.write_text('x,y\n1,2\n3,4\n',encoding='utf-8')
        profile=Client().run('data.profile',data=csv_path)
        assert profile.data['columns']['x']['mean']==2
        profile.export(Path(tmp)/'profile.json')
        file=Path(tmp)/'note.txt';file.write_text('Local AI helps researchers.',encoding='utf-8')
        flow=AgentTeam().run([Step('read','document.read',{'document':file}),Step('summary','text.analyze',{'text':Ref('read','text')})])
        assert flow.data['results']['summary']['data']['words']==4
    evidence={'wheel_version':dist.version,'python':sys.version.split()[0],'mandatory_runtime_dependencies':mandatory,'capability_count':len(Client().capabilities()),'checks':['wheel import outside checkout','no mandatory runtime dependencies','real text analysis','CSV statistics and export','lexical retrieval','agent reference data flow'],'model_inference_tested':False,'passed':True}
    Path(args.output).write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    print(json.dumps(evidence,indent=2))

if __name__=='__main__':main()
