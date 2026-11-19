"""Real optional-engine integration tests on generated, clearly labeled fixtures."""
import csv
import io
import wave
from pathlib import Path
import pytest
from alfarouqai import Client, Config, ValidationError, ConsentRequired

ROOT=Path(__file__).resolve().parents[1]


def make_training(tmp_path, regression=False):
    p=tmp_path/'training.csv'
    with p.open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['hours','attendance','track','target'])
        for i in range(120):
            h=1+i%10; attendance=50+(i*7)%51
            target=h*6+attendance*.4 if regression else ('yes' if h>=6 else 'no')
            w.writerow([h,attendance,['arts','science'][i%2],target])
    return p


@pytest.mark.optional
@pytest.mark.parametrize('problem',['classification','regression'])
def test_train_and_predict(tmp_path,problem):
    pytest.importorskip('sklearn'); pytest.importorskip('pandas')
    p=make_training(tmp_path,problem=='regression')
    trained=Client().train(data=p,target='target',problem=problem)
    assert trained.report.data['train_rows']==90
    assert trained.report.data['test_rows']==30
    assert len(trained.report.data['rows'])==30
    prediction=trained.predict([{'hours':8,'attendance':90,'track':'unseen-category'}])
    assert len(prediction.data['rows'])==1
    if problem=='classification':
        assert trained.report.data['metrics']['accuracy']>=.9
    else:
        assert trained.report.data['metrics']['mae']<8
    with pytest.raises(ValidationError): trained.predict([{'hours':8}])
    with pytest.raises(ConsentRequired): trained.save(tmp_path/'model.skops')


@pytest.mark.optional
def test_report_api_and_natural_language_ml(tmp_path):
    pytest.importorskip('sklearn'); pytest.importorskip('pandas')
    p=make_training(tmp_path)
    result=Client()('train model',data=p,target='target',problem='classification')
    assert result.task=='ml.train' and result.provenance['executed']


@pytest.mark.optional
def test_classification_reproducible(tmp_path):
    pytest.importorskip('sklearn'); pytest.importorskip('pandas')
    p=make_training(tmp_path)
    a=Client().train(data=p,target='target',problem='classification')
    b=Client().train(data=p,target='target',problem='classification')
    assert a.report.data==b.report.data


@pytest.mark.optional
def test_no_target_in_features(tmp_path):
    pytest.importorskip('sklearn'); pytest.importorskip('pandas')
    trained=Client().train(data=make_training(tmp_path),target='target',problem='classification')
    assert 'target' not in trained.features
    assert set(trained.features)=={'hours','attendance','track'}


@pytest.mark.optional
def test_image_on_founder_photo():
    pytest.importorskip('cv2')
    p=ROOT/'identity/founder/khalid-salman-original.jpg'
    result=Client().run('image.analyze',image=p)
    assert result.data['width']==720
    assert result.data['height']==1600
    assert result.data['face_count']>=1
    assert result.provenance['input_sha256']


@pytest.mark.optional
def test_invalid_image(tmp_path):
    pytest.importorskip('cv2')
    p=tmp_path/'bad.jpg'; p.write_text('not a photo')
    with pytest.raises(ValidationError): Client().run('image.analyze',image=p)


@pytest.mark.optional
def test_motion_video(tmp_path):
    cv2=pytest.importorskip('cv2'); np=pytest.importorskip('numpy')
    p=tmp_path/'motion.avi'
    writer=cv2.VideoWriter(str(p),cv2.VideoWriter_fourcc(*'MJPG'),10,(160,120))
    assert writer.isOpened(), 'Test codec unavailable'
    for i in range(15):
        frame=np.zeros((120,160,3),dtype=np.uint8)
        cv2.rectangle(frame,(i*5,40),(i*5+30,75),(255,255,255),-1)
        writer.write(frame)
    writer.release()
    r=Client(Config(max_video_frames=10)).run('video.motion',video=p,min_area=20)
    assert r.data['processed_frames']==10 and r.data['truncated'] is True
    assert any(row['boxes'] for row in r.data['rows'][1:])


def test_pcm_wav(tmp_path):
    p=tmp_path/'silence.wav'
    with wave.open(str(p),'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(16000)
        f.writeframes(b'\0\0'*16000)
    result=Client().run('audio.info',audio=p)
    assert result.data['duration_seconds']==1
    assert result.data['sample_rate']==16000


@pytest.mark.optional
def test_docx_real_roundtrip(tmp_path):
    docx=pytest.importorskip('docx')
    p=tmp_path/'sample.docx'; d=docx.Document(); d.add_paragraph('خالد سلمان AlFarouq AI')
    t=d.add_table(rows=1,cols=2); t.cell(0,0).text='key'; t.cell(0,1).text='value'
    d.save(p)
    r=Client().run('document.read',document=p)
    assert 'خالد سلمان' in r.data['text'] and 'key\tvalue' in r.data['text']


@pytest.mark.optional
def test_xlsx_real_roundtrip(tmp_path):
    xl=pytest.importorskip('openpyxl')
    p=tmp_path/'sample.xlsx'; b=xl.Workbook(); s=b.active; s.title='students'
    s.append(['name','score']); s.append(['خالد',95]); b.save(p)
    r=Client().run('document.read',document=p)
    assert len(r.data['rows'])==2 and '95' in r.data['text']


@pytest.mark.optional
def test_pdf_real_text_extraction(tmp_path):
    pytest.importorskip('pypdf')
    pytest.importorskip('reportlab')
    from reportlab.pdfgen import canvas
    p=tmp_path/'sample.pdf'; c=canvas.Canvas(str(p)); c.drawString(72,720,'AlFarouq AI real PDF fixture'); c.save()
    r=Client().run('document.read',document=p)
    assert 'AlFarouq AI real PDF fixture' in r.data['text']


@pytest.mark.optional
def test_office_archive_bomb_guard(tmp_path):
    import zipfile
    pytest.importorskip('docx')
    p=tmp_path/'huge.docx'
    with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_DEFLATED) as z: z.writestr('huge','x'*100_000)
    with pytest.raises(ValidationError,match='expansion'):
        Client(Config(max_input_bytes=1000)).run('document.read',document=p)
