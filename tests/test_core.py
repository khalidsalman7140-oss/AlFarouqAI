"""Offline core tests. No paid services, model downloads or external requests."""
import csv
import importlib
import json
import subprocess
import sys
from pathlib import Path
import pytest
from alfarouqai import (AI, Client, Config, Result, Capability, Registry, ValidationError,
                       MissingDependency, ConsentRequired, UnsupportedTask,
                       AgentTeam, Step, Ref, KnowledgeBase)
from alfarouqai.core import require
from alfarouqai.dependencies import doctor, install_extra, installation_plan

ROOT = Path(__file__).resolve().parents[1]


def test_import_is_lightweight():
    script = 'import alfarouqai,sys; assert not any(x in sys.modules for x in ["torch","sklearn","cv2","pandas","transformers","pypdf"]); print("lightweight")'
    p = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


def test_text_arabic():
    r = AI('حلل هذا النص', text='الذكاء الاصطناعي مفيد. Python is useful!')
    assert r.task == 'text.analyze'
    assert r.data['words'] == 6
    assert r.provenance['executed'] is True
    assert 'الذكاء' in r.data['extractive_summary']


def test_empty_text():
    r = Client().run('text.analyze', text='')
    assert r.data['words'] == 0


def test_unknown_input_not_silently_ignored():
    with pytest.raises(ValidationError, match='Unknown inputs'):
        Client().run('text.analyze', text='hi', target='wrong')


@pytest.mark.parametrize('kwargs', [{'max_rows':0}, {'timeout':float('nan')}, {'max_agent_steps':-1}, {'allow_network':'false'}, {'max_rows':True}])
def test_invalid_config(kwargs):
    with pytest.raises(ValidationError): Config(**kwargs)


def test_config_roundtrip(tmp_path):
    path=tmp_path/'config.json'; Config().save(path)
    assert Config.load(path) == Config()
    with pytest.raises(FileExistsError): Config().save(path)


def test_unknown_config_key(tmp_path):
    p=tmp_path/'c.json'; p.write_text('{"bogus":true}')
    with pytest.raises(ValidationError): Config.load(p)


@pytest.mark.parametrize('ext',['json','csv','md','html','txt'])
def test_exports(tmp_path,ext):
    result=Client().run('text.analyze',text='السلام عليكم. Hello world.')
    path=result.export(tmp_path/f'report.{ext}')
    assert path.stat().st_size>20
    with pytest.raises(FileExistsError): result.export(path)
    result.export(path,overwrite=True)
    if ext=='json': assert json.loads(path.read_text())['task']=='text.analyze'


def test_html_escaping(tmp_path):
    p=Result('test',{'value':'<script>alert(1)</script>'},'test').export(tmp_path/'r.html')
    assert '<script>' not in p.read_text()
    assert '&lt;script&gt;' in p.read_text()


def test_csv_formula_guard(tmp_path):
    p=Result('test',{'rows':[{'a':'=2+2','b':'  @SUM(A1)','c':-5}]},'test').export(tmp_path/'r.csv')
    with p.open(newline='') as f: row=next(csv.DictReader(f))
    assert row['a'].startswith("'") and row['b'].startswith("'")
    assert row['c']=='-5'


def test_nonfinite_json(tmp_path):
    p=Result('t',{'n':float('nan')},'t').export(tmp_path/'r.json')
    assert json.loads(p.read_text())['data']['n'] is None


def test_invalid_export(tmp_path):
    with pytest.raises(ValidationError): Result('t',{},'x').export(tmp_path/'r.exe')


def test_data_profile():
    r=AI('حلل البيانات',data=ROOT/'examples/data/students.csv')
    assert r.data['row_count']==100
    assert r.data['columns']['study_hours']['mean']==5.5


@pytest.mark.parametrize('content',['a,a\n1,2\n','a,b\n1\n','a,b\n1,2,3\n','a,b\n'])
def test_invalid_csv(tmp_path,content):
    p=tmp_path/'x.csv'; p.write_text(content)
    with pytest.raises(ValidationError): Client().run('data.profile',data=p)


def test_csv_row_budget():
    with pytest.raises(ValidationError): Client(Config(max_rows=2)).run('data.profile',data=ROOT/'examples/data/students.csv')


def test_missing_file(tmp_path):
    with pytest.raises(ValidationError): Client().run('document.read',document=tmp_path/'none.txt')


def test_text_file():
    r=Client().run('document.read',document=ROOT/'examples/data/knowledge.txt')
    assert 'خالد' in r.data['text']


def test_sensor_outlier():
    r=Client().run('iot.analyze',data=ROOT/'examples/data/sensors.csv',column='temperature')
    flagged=[row for row in r.data['rows'] if row['anomaly']]
    assert len(flagged)==1 and flagged[0]['row']==25


def test_defensive_logs():
    r=Client().run('security.logs',path=ROOT/'examples/data/auth.log')
    assert r.data['failed_auth_by_source']['192.0.2.10']==2


def test_code_does_not_execute(tmp_path):
    destination=tmp_path/'must-not-exist'
    source=f'import os\nos.system(\'mkdir "{destination.as_posix()}"\')\nsecret="redact-me"\n'
    r=Client().run('code.analyze',code=source)
    assert not destination.exists()
    assert {'dangerous-call','possible-secret'} <= {f['rule'] for f in r.data['findings']}
    assert 'redact-me' not in json.dumps(r.to_dict())


def test_ast_alias_and_syntax():
    r=Client().run('code.analyze',code='from pickle import loads as load\nload(data)\n')
    assert r.data['findings'][0]['rule']=='dangerous-call'
    r=Client().run('code.analyze',code='def broken(:')
    assert r.data['findings'][0]['rule']=='syntax-error'


def test_code_project_skips_venv(tmp_path):
    (tmp_path/'main.py').write_text('def x():\n    return 3\n')
    (tmp_path/'.venv').mkdir(); (tmp_path/'.venv/no.py').write_text('eval(data)')
    r=Client().run('code.analyze',path=tmp_path)
    assert r.data['parsed_files']==1 and r.data['findings']==[]


def test_code_inputs():
    with pytest.raises(ValidationError): Client().run('code.analyze')


def test_unknown_task():
    with pytest.raises(UnsupportedTask): Client().run('invented')


def test_router_refuses_missing_target():
    plan=Client().plan('أنشئ نموذج تعلم آلة للتنبؤ بالنتائج',data='data.csv')
    assert set(plan['missing'])=={'target','problem'}
    with pytest.raises(ValidationError): AI('أنشئ نموذج للتنبؤ',data='data.csv')


def test_router_no_false_tracking():
    with pytest.raises(UnsupportedTask): AI('حلل هذا الفيديو واكتشف الأشخاص وحركاتهم',video='v.mp4')


def test_router_requires_objects_model():
    with pytest.raises(ValidationError,match='model_path'): AI('حلل هذه الصورة واكتشف الأشياء الموجودة فيها',image='p.jpg')


def test_router_ambiguous():
    with pytest.raises(UnsupportedTask): AI('حلل',data='a.csv',image='a.jpg')


def test_router_unknown_text_generation():
    with pytest.raises(UnsupportedTask): AI('translate',text='hello')


def test_missing_dependency(monkeypatch):
    original=importlib.import_module
    def blocked(name):
        if name=='absent_package': raise ImportError(name)
        return original(name)
    monkeypatch.setattr(importlib,'import_module',blocked)
    with pytest.raises(MissingDependency,match='Nothing was installed'):
        require('absent_package','ml')


def test_registry_plugin():
    reg=Registry()
    reg.register(Capability('custom',lambda *,text,config:Result('custom',{'value':text},'custom'),'test',('text',)))
    assert Client(registry=reg).run('custom',text='yes').data['value']=='yes'
    with pytest.raises(ValidationError): reg.register(reg.get('custom'))
    with pytest.raises(ConsentRequired): reg.load_plugins()


def test_kb_search_roundtrip(tmp_path):
    kb=KnowledgeBase(chunk_size=80,overlap=10)
    kb.add('Python packaging supports optional dependencies.',source='packaging')
    kb.add('خالد سلمان مؤسس المشروع.',source='founder')
    assert kb.search('خالد').data['rows'][0]['source']=='founder'
    assert kb.search('optional dependencies').data['rows'][0]['source']=='packaging'
    assert kb.search('zzzzzz').data['rows']==[]
    kb.save(tmp_path/'index.json')
    assert KnowledgeBase.load(tmp_path/'index.json').search('خالد').data['rows']


def test_kb_overlap_offsets():
    kb=KnowledgeBase(chunk_size=40,overlap=10)
    kb.add('a'*90,source='one')
    assert [c['start'] for c in kb.chunks]==[0,30,60]
    with pytest.raises(ValidationError): KnowledgeBase(chunk_size=40,overlap=40)
    with pytest.raises(ValidationError): kb.search('')


def test_agent_data_flow():
    steps=[Step('read','document.read',{'document':ROOT/'examples/data/knowledge.txt'}),Step('summary','text.analyze',{'text':Ref('read','text')})]
    r=AgentTeam(workers=2).run(steps)
    assert r.data['levels']==[['read'],['summary']]
    assert r.data['results']['summary']['data']['words']>10
    assert any(e['agent']=='schema-reviewer' for e in r.data['trace'])


def test_agent_cycle():
    with pytest.raises(ValidationError,match='cycle'):
        AgentTeam().run([Step('a','text.analyze',{'text':Ref('b','text')}),Step('b','text.analyze',{'text':Ref('a','text')})])


def test_agent_tool_allowlist():
    with pytest.raises(ConsentRequired): AgentTeam().run([Step('a','llm.chat',{'prompt':'hi'})])


def test_agent_step_budget():
    with pytest.raises(ValidationError): AgentTeam(Client(Config(max_agent_steps=1))).run([Step('a','text.analyze',{'text':'a'}),Step('b','text.analyze',{'text':'b'})])


def test_agent_bad_reference():
    with pytest.raises(ValidationError): AgentTeam().run([Step('a','text.analyze',{'text':'x'}),Step('b','text.analyze',{'text':Ref('a','nonexistent')})])


def test_agent_parallel_independent():
    r=AgentTeam(workers=2).run([Step('a','text.analyze',{'text':'one'}),Step('b','text.analyze',{'text':'two'})])
    assert r.data['levels']==[['a','b']]


def test_installer_requires_consent(tmp_path):
    with pytest.raises(ConsentRequired): install_extra('vision',tmp_path/'env')
    assert not (tmp_path/'env').exists()


def test_installer_rejects_foreign_directory(tmp_path):
    with pytest.raises(ValidationError): install_extra('vision',tmp_path,consent=True)


def test_installer_allowlist():
    with pytest.raises(ValidationError): installation_plan('anything;rm','/tmp/test')
    p=installation_plan('vision','./new-env')
    assert p['command'][1:4]==['-m','pip','--isolated']
    assert p['packages']==['opencv-python-headless>=4.10,<5']


def test_doctor_has_no_network():
    assert doctor()['network_on_import'] is False


def test_cli(capsys):
    from alfarouqai.cli import main
    assert main(['run','text.analyze','--inputs','{"text":"hello"}'])==0
    assert json.loads(capsys.readouterr().out)['data']['words']==1
    assert main(['run','no-such-task'])==2
    assert 'UnsupportedTask' in capsys.readouterr().err


def test_cli_plan_no_execution(capsys):
    from alfarouqai.cli import main
    assert main(['plan','حلل البيانات','--inputs','{"data":"does-not-exist.csv"}'])==0
    assert json.loads(capsys.readouterr().out)['executes'] is False
