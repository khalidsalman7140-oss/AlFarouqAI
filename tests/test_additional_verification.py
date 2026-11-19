"""Close remaining original-release gaps and exercise new dispatch wrappers."""
import json
import os
import subprocess
from pathlib import Path
import pytest
from alfarouqai import Client, Config, Scheduler
ROOT=Path(__file__).resolve().parents[1]


def test_automation_public_dispatch(tmp_path):
    path=tmp_path/'jobs.sqlite';scheduler=Scheduler(path)
    scheduler.add('one','text.analyze',{'text':'hello'},run_at=0);scheduler.close()
    result=Client().run('automation.tick',store=path,now=1)
    assert result.data['rows'][0]['status']=='completed'


@pytest.mark.optional
def test_original_skops_save_actually_runs(tmp_path):
    pytest.importorskip('skops.io');pytest.importorskip('sklearn')
    p=tmp_path/'train.csv';p.write_text('x,label\n'+'\n'.join(f'{i},{i%2}' for i in range(40)))
    model=Client().train(data=p,target='label',problem='classification')
    output=model.save(tmp_path/'model.skops',consent=True)
    assert output.stat().st_size>1000
    import zipfile
    with zipfile.ZipFile(output) as z:assert z.testzip() is None


@pytest.mark.system
@pytest.mark.skipif(os.environ.get('ALFAROUQ_RUN_MODELS')!='1',reason='Explicit network-test approval required')
def test_real_dedicated_venv_installer_success(tmp_path):
    from alfarouqai.dependencies import install_extra
    output=install_extra('iot',tmp_path/'managed-environment',consent=True,timeout=120)
    assert output['returncode']==0
    exe=output['command'][0]
    p=subprocess.run([exe,'-c','import serial,paho.mqtt.client; print("transport imports verified")'],capture_output=True,text=True,timeout=20)
    assert p.returncode==0
    path=ROOT/'reports/installer-success-0.2.json'
    path.write_text(json.dumps({'extra':'iot','dedicated_venv':True,'pip_returncode':0,'installed_imports_tested':['serial','paho.mqtt.client'],'no_current_interpreter_mutation':True},indent=2))


@pytest.mark.model
@pytest.mark.skipif(os.environ.get('ALFAROUQ_RUN_MODELS')!='1',reason='Prepared trained weights required')
def test_new_public_dispatch_and_original_semantic_adapter(tmp_path):
    from alfarouqai import SemanticIndex
    from alfarouqai.models import prepare
    client=Client()
    result=client.run('nlp.classify',text='This is excellent.',labels=['positive','negative'])
    assert result.data['label'] in ('positive','negative')
    document=tmp_path/'fact.txt';document.write_text('A temperature sensor measures heat. Students use Python for AI.')
    store=tmp_path/'public.sqlite'
    assert client.run('rag.index',document=document,store=store).data['chunks_added']>0
    assert client.run('rag.search.semantic',store=store,query='measuring temperature').data['rows']
    assert client.run('rag.answer',store=store,question='What measures heat?').data['sources']
    result=client.run('agents.llm',goal='Analyze text statistics.',inputs_by_task={'text.analyze':{'text':'Python helps students.'}})
    assert result.data['review']
    model=prepare('minilm-multilingual')
    semantic=SemanticIndex(str(model));semantic.add('A temperature sensor measures heat.',source='fact')
    assert semantic.search('temperature measurement').data['rows'][0]['source']=='fact'
