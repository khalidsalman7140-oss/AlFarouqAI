"""Practical-service acceptance, validation and safety boundaries."""
import csv
import json
import math
import sqlite3
from pathlib import Path
import pytest
from alfarouqai import AI,Client,Config,ValidationError,ConsentRequired


def csv_file(path,header,rows):
    with path.open('w',newline='',encoding='utf-8') as stream:
        writer=csv.writer(stream);writer.writerow(header);writer.writerows(rows)
    return path


def test_shortcuts_logging_and_file_insights(tmp_path,capsys):
    doc=tmp_path/'report.txt';doc.write_text('Python helps students. Date: 2026-11-16. Contact example@example.com.')
    r=AI('حلل هذا الملف واستخرج أهم المعلومات',file=doc,config=Config(verbose=True))
    assert r.task=='document.insights' and r.data['dates_found']==['2026-11-16']
    assert 'start task=document.insights' in capsys.readouterr().err
    assert Client().file(doc).data['words']>2
    assert AI('ar',text='العَرَبِيَّةُ',stem=False).data['normalized']=='العربية'


def test_logging_error_does_not_dump_input(capsys):
    with pytest.raises(ValidationError):Client(Config(verbose=True)).run('text.analyze',text=3)
    log=capsys.readouterr().err;assert 'type=ValidationError' in log and 'text=3' not in log


@pytest.mark.optional
def test_arabic_stemmer_and_text_training(tmp_path):
    pytest.importorskip('nltk');pytest.importorskip('sklearn')
    r=Client().ar('يكتب الطلاب دروس العربية في المدارس')
    assert len(r.data['stems'])>2 and 'في' not in r.data['filtered_tokens']
    p=csv_file(tmp_path/'corpus.csv',['text','label'],[(f'خدمة ممتازة رائعة وسريعة تجربة رقم {i}','positive') for i in range(24)]+[(f'خدمة سيئة بطيئة ومزعجة تجربة رقم {i}','negative') for i in range(24)])
    model=Client().text_train(data=p,text_column='text',target='label')
    assert model.report.data['train_rows']==36 and model.report.data['accuracy']>=.8
    assert model.predict(['خدمة ممتازة رائعة']).data['rows'][0]['prediction']=='positive'
    assert Client().run('nlp.train',data=p,text_column='text',target='label').task=='nlp.train'
    assert Client().run('nlp.topics',data=p,text_column='text',n_topics=2).data['rows']
    assert Client().run('nlp.similarity',texts=['تعلم لغة بايثون','إصلاح مضخة صناعية'],query='بايثون').data['rows'][0]['index']==0


@pytest.mark.optional
def test_text_classifier_conflicting_duplicates(tmp_path):
    pytest.importorskip('sklearn')
    p=csv_file(tmp_path/'bad.csv',['t','y'],[('same','a'),('same','b')]+[(f'word {i}',str(i%2)) for i in range(20)])
    with pytest.raises(ValidationError,match='Conflicting'):Client().text_train(data=p,text_column='t',target='y')


@pytest.mark.optional
def test_monthly_forecast_and_calendar_validation(tmp_path):
    pytest.importorskip('pandas')
    rows=[(f'{2024+i//12}-{i%12+1:02d}-01',100+i*10) for i in range(24)]
    p=csv_file(tmp_path/'sales.csv',['date','sales'],rows)
    r=AI('حلل المبيعات وتوقع مبيعات الشهر القادم',data=p)
    assert r.task=='sales.forecast' and r.data['rows'][0]['month']=='2026-01' and abs(r.data['rows'][0]['forecast']-340)<1e-7
    bad=csv_file(tmp_path/'bad.csv',['date','sales'],rows[:4]+rows[5:])
    with pytest.raises(ValidationError,match='gaps'):Client().sales(bad)
    bad=csv_file(tmp_path/'bad2.csv',['date','sales'],[('2024-02-31',1)]+rows[1:])
    with pytest.raises(ValidationError):Client().sales(bad)


def test_clean_privacy_group_reconcile(tmp_path):
    p=csv_file(tmp_path/'data.csv',['department','value'],[(' Lab ','2'),('Lab','2'),('Clinic','3')])
    assert Client().run('data.clean',data=p).data['duplicates_removed']==1
    assert Client().run('data.group',data=p,group_column='department',value_column='value').data['rows']
    r=AI('redact',text='Contact user@example.org +967 700 123 456')
    assert '[EMAIL]' in r.data['text'] and '[PHONE]' in r.data['text']
    a=csv_file(tmp_path/'a.csv',['id','amount'],[('a','0.30'),('b','7.00')]);b=csv_file(tmp_path/'b.csv',['id','amount'],[('a','.3'),('c','8')])
    result=Client().run('finance.reconcile',left=a,right=b,key='id',amount_column='amount')
    assert result.data['counts']=={'matched':1,'missing-right':1,'missing-left':1}


@pytest.mark.optional
def test_industrial_features_control_and_production(tmp_path):
    pytest.importorskip('numpy')
    rate=100;p=csv_file(tmp_path/'sensor.csv',['vibration'],[(math.sin(2*math.pi*10*i/rate),) for i in range(100)])
    r=AI('sensors',data=p,columns=['vibration'],sample_rate=rate)
    assert abs(r.data['rows'][0]['dominant_frequency_hz']-10)<1e-8
    baseline=csv_file(tmp_path/'baseline.csv',['temperature'],[(20+i%3,) for i in range(30)])
    current=csv_file(tmp_path/'current.csv',['temperature'],[(21,),(50,)])
    r=Client().run('industry.control',data=current,column='temperature',baseline=baseline)
    assert not r.data['rows'][0]['out_of_control'] and r.data['rows'][1]['out_of_control']
    production=csv_file(tmp_path/'production.csv',['total','good'],[(100,95),(200,190)])
    r=Client().run('industry.production',data=production,total_column='total',good_column='good',operating_hours=3)
    assert r.data['yield_fraction']==.95 and r.data['units_per_operating_hour']==100


@pytest.mark.optional
def test_actual_quality_difference_not_generic_object_detection(tmp_path):
    cv2=pytest.importorskip('cv2');np=pytest.importorskip('numpy')
    good=np.full((128,128,3),255,dtype=np.uint8);bad=good.copy();cv2.rectangle(bad,(35,45),(65,75),(0,0,0),-1)
    a=tmp_path/'good.png';b=tmp_path/'bad.png';cv2.imwrite(str(a),good);cv2.imwrite(str(b),bad)
    r=AI('اكتشف العيوب الموجودة في المنتج',image=b,reference=a)
    assert r.task=='industry.defects' and r.data['candidate_count']==1
    assert Client().inspect(a,a).data['candidate_count']==0
    with pytest.raises(ValidationError,match='reference'):AI('اكتشف العيوب',image=b)


@pytest.mark.optional
def test_labeled_maintenance_and_database_read_only(tmp_path):
    pytest.importorskip('sklearn')
    p=csv_file(tmp_path/'maintenance.csv',['temperature','vibration','failure'],[(20+i,1+i%5,'yes' if i>=25 else 'no') for i in range(50)])
    assert Client().run('industry.maintenance',data=p,target='failure').data['metrics']
    db=tmp_path/'factory.sqlite';c=sqlite3.connect(db);c.execute('CREATE TABLE readings(id INTEGER PRIMARY KEY,value REAL)');c.execute('INSERT INTO readings VALUES(1,2)');c.commit();c.close()
    before=db.read_bytes();r=AI('db',database=db)
    assert r.data['rows'][0]['row_count']==1 and before==db.read_bytes()


def test_grid_search_found_and_unreachable():
    assert AI('astar',grid=[[0,0,0],[0,1,0]],start=[0,0],goal=[1,2]).data['cost']==3
    assert not AI('astar',grid=[[0,1,0]],start=[0,0],goal=[0,2]).data['found']


@pytest.mark.optional
def test_numpy_result_export_handles_multidimensional_arrays(tmp_path):
    np=pytest.importorskip('numpy');from alfarouqai import Result
    p=Result('test',{'matrix':np.array([[1,2],[3,4]])},'numpy').export(tmp_path/'array.json')
    assert json.loads(p.read_text())['data']['matrix']==[[1,2],[3,4]]


@pytest.mark.optional
def test_api_auth_allowlist_and_errors():
    pytest.importorskip('fastapi');pytest.importorskip('httpx')
    from fastapi.testclient import TestClient
    from alfarouqai.api import create_app
    app=create_app(token='test-only-bearer-token');c=TestClient(app)
    assert c.get('/health').status_code==200
    assert c.post('/v1/run',json={'task':'text.analyze','inputs':{'text':'hello'}}).status_code==401
    headers={'Authorization':'Bearer test-only-bearer-token'}
    assert c.post('/v1/run',headers=headers,json={'task':'text.analyze','inputs':{'text':'hello'}}).json()['data']['words']==1
    assert c.post('/v1/run',headers=headers,json={'task':'code.test','inputs':{'path':'.'}}).status_code==403
    assert c.post('/v1/run',headers=headers,json={'task':'text.analyze','inputs':{'text':7}}).status_code==422
    assert Client().run('api.schema').data['openapi']['paths']
