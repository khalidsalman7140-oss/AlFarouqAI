"""Incremental 0.2 tests; all original tests remain unchanged."""
import json
from pathlib import Path
import pytest
from alfarouqai import Client, Config, AI, Scheduler, ConsentRequired, ValidationError, prepare_model, model_inventory


def test_new_registry_keeps_old_tasks():
    names={c['name'] for c in Client().capabilities()}
    assert {'text.analyze','ml.train','image.objects','llm.chat','vision.detect','deep.train','rag.answer','robotics.serial'}<=names
    assert len(names)>=40


def test_explicit_one_line():
    assert AI('text.analyze',text='Hello world').data['words']==2
    assert AI('not parsed, explicitly chosen',task='text.analyze',text='Hello').data['words']==1


def test_model_consent(tmp_path,monkeypatch):
    monkeypatch.setenv('ALFAROUQ_MODEL_HOME',str(tmp_path))
    with pytest.raises(ConsentRequired):prepare_model('smollm2-135m')
    assert not (tmp_path/'smollm2-135m').exists()
    with pytest.raises(ValidationError):prepare_model('untrusted-user-repo')


def test_prepare_dependency_plan(tmp_path):
    plan=Client().prepare('vision.detect',tmp_path/'env')
    assert 'torchvision' in str(plan['packages'])
    assert not (tmp_path/'env').exists()


def test_generation_adapters_not_claimed_as_tested():
    for name in ('image.generate','video.generate'):
        assert Client().registry.get(name).status=='adapter-not-runtime-tested'
        with pytest.raises(ConsentRequired):Client().run(name,prompt='test',model_path='missing',output='out.png')


def test_device_and_code_execution_opt_in():
    for name,inputs in [('robotics.serial',{'port':'/dev/invalid'}),('iot.mqtt.publish',{'host':'localhost','topic':'a','message':'x'}),('code.test',{'path':'.'})]:
        with pytest.raises(ConsentRequired):Client().run(name,**inputs)
    with pytest.raises(ConsentRequired):Client().run('iot.mqtt.read',host='localhost',topic='a')


def test_scheduler_persistence_and_once(tmp_path):
    path=tmp_path/'jobs.db';s=Scheduler(path)
    s.add('one','text.analyze',{'text':'hello world'},run_at=10)
    s.close();s=Scheduler(path)
    assert s.tick(now=9).data['rows']==[]
    assert s.tick(now=10).data['rows'][0]['result']['data']['words']==2
    assert s.tick(now=11).data['rows']==[]
    assert s.jobs()[0]['status']=='completed';s.close()


def test_scheduler_cancel_fail_and_guard(tmp_path):
    s=Scheduler(tmp_path/'jobs.db')
    with pytest.raises(ConsentRequired):s.add('net','llm.chat',{},run_at=0)
    s.add('cancel','text.analyze',{'text':'a'},run_at=0);s.cancel('cancel')
    s.add('bad','data.profile',{'data':'does-not-exist.csv'},run_at=0)
    out=s.tick(now=1).data['rows'];assert len(out)==1 and out[0]['status']=='failed'
    s.close()


def test_agent_guard_before_model_load():
    from alfarouqai import LLMAgent
    with pytest.raises(ConsentRequired):LLMAgent().run('control robot',inputs_by_task={'robotics.serial':{'port':'x'}})


def test_centroid_tracker_real_association():
    from alfarouqai.vision import CentroidTracker
    tracker=CentroidTracker(max_distance=50)
    one=tracker.update([{'label':'person','box_xyxy':[0,0,20,30],'score':.9}])
    two=tracker.update([{'label':'person','box_xyxy':[5,0,25,30],'score':.9}])
    assert one[0]['track_id']==two[0]['track_id']
    three=tracker.update([{'label':'cat','box_xyxy':[5,0,25,30],'score':.9}])
    assert three[0]['track_id']!=two[0]['track_id']


@pytest.mark.optional
def test_forecast(tmp_path):
    pytest.importorskip('numpy')
    p=tmp_path/'trend.csv';p.write_text('y\n'+'\n'.join(str(2*i+3) for i in range(30)))
    r=Client().run('data.forecast',data=p,column='y',horizon=3)
    assert r.data['holdout_mae']<1e-8 and abs(r.data['rows'][0]['prediction']-63)<1e-8


@pytest.mark.optional
def test_recommendations(tmp_path):
    pytest.importorskip('numpy')
    p=tmp_path/'ratings.csv';p.write_text('user,item,rating\nu1,a,5\nu1,b,4\nu2,a,5\nu2,b,4\nu2,c,5\nu3,d,5\n')
    r=Client().run('data.recommend',data=p,user='u1',user_column='user',item_column='item',rating_column='rating')
    assert r.data['rows'][0]['item']=='c'


@pytest.mark.optional
def test_isolation_forest(tmp_path):
    pytest.importorskip('sklearn')
    p=tmp_path/'anomaly.csv';p.write_text('x,y\n'+'\n'.join(f'{i%4},{i%3}' for i in range(50))+'\n100,100\n')
    r=Client().run('security.anomalies',data=p,columns=['x','y'])
    assert r.data['rows'][-1]['anomaly']


@pytest.mark.optional
def test_neural_training_save_load(tmp_path):
    pytest.importorskip('torch');pytest.importorskip('safetensors')
    from alfarouqai import NeuralModel
    p=tmp_path/'train.csv';p.write_text('x,y,target\n'+'\n'.join(f'{i%10},{i//10},{int(i%10>=5)}' for i in range(100)))
    model=Client().deep_train(data=p,target='target',problem='classification',epochs=40)
    assert model.report.data['final_loss']<model.report.data['initial_loss']
    assert model.report.data['metrics']['accuracy']>=.8
    a=model.predict([{'x':8,'y':5}]).data
    model.save(tmp_path/'network')
    restored=NeuralModel.load(tmp_path/'network',config=Config())
    assert restored.predict([{'x':8,'y':5}]).data==a


@pytest.mark.optional
def test_neural_regression(tmp_path):
    pytest.importorskip('torch')
    p=tmp_path/'train.csv';p.write_text('x,target\n'+'\n'.join(f'{i/10},{i/5+1}' for i in range(80)))
    r=Client().run('deep.train',data=p,target='target',problem='regression',epochs=80)
    assert r.data['final_loss']<r.data['initial_loss']


def test_trusted_unittest_runner(tmp_path):
    (tmp_path/'test_math.py').write_text('import unittest\nclass TestMath(unittest.TestCase):\n def test_add(self):self.assertEqual(1+1,2)\n')
    r=Client().run('code.test',path=tmp_path,consent=True)
    assert r.data['passed'] is True and 'OK' in r.data['log']
