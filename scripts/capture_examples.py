"""Capture verifiable local result artifacts; no external inference or network."""
from pathlib import Path
import csv
import json
import tempfile
import wave
from alfarouqai import Client, Config, AgentTeam, Step, Ref, KnowledgeBase

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/real-results'

def save(result,name):
    OUT.mkdir(parents=True,exist_ok=True)
    return result.export(OUT/name,overwrite=True)

def main():
    import cv2
    import numpy as np
    from docx import Document
    from openpyxl import Workbook
    from reportlab.pdfgen import canvas
    client=Client()
    save(client.run('text.analyze',text='الذكاء الاصطناعي يساعد الطلاب. Local tools support research.'),'text.json')
    save(client.run('data.profile',data=ROOT/'examples/data/students.csv'),'data-profile.json')
    save(client.run('code.analyze',path=ROOT/'src/alfarouqai'),'source-review.json')
    save(client.run('security.logs',path=ROOT/'examples/data/auth.log'),'defensive-logs.json')
    save(client.run('iot.analyze',data=ROOT/'examples/data/sensors.csv',column='temperature'),'sensors.json')
    save(client.run('image.analyze',image=ROOT/'identity/founder/khalid-salman-original.jpg'),'founder-photo-analysis.json')
    team=AgentTeam(workers=2).run([Step('read','document.read',{'document':ROOT/'examples/data/knowledge.txt'}),Step('summary','text.analyze',{'text':Ref('read','text')})])
    save(team,'agents.json')
    kb=KnowledgeBase(chunk_size=140,overlap=20);kb.add((ROOT/'examples/data/knowledge.txt').read_text(),source='knowledge.txt')
    save(kb.search('خالد سلمان'),'lexical-retrieval.json')
    with tempfile.TemporaryDirectory() as temp:
        tmp=Path(temp)
        train=tmp/'train.csv'
        with (ROOT/'examples/data/students.csv').open() as f:
            rows=[{k:v for k,v in row.items() if k!='score'} for row in csv.DictReader(f)]
        with train.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        trained=client.train(data=train,target='passed',problem='classification')
        trained.report.warnings.append('Synthetic teaching fixture only. A high score is not evidence of real-world generalization.')
        save(trained.report,'classification.json')
        save(trained.predict([{'study_hours':7,'attendance':90,'track':'science'}]),'predictions.json')
        with train.open('w',newline='') as f:
            w=csv.writer(f);w.writerow(['x','group','target'])
            for i in range(120):w.writerow([i,'a' if i%2 else 'b',i*2+3])
        reg=client.train(data=train,target='target',problem='regression')
        reg.report.warnings.append('Synthetic y=2x+3 fixture, not a research benchmark.')
        save(reg.report,'regression.json')
        for ext in ('csv','md','html','txt'):
            trained.report.export(OUT/f'classification-report.{ext}',overwrite=True)
        wav=tmp/'fixture.wav'
        with wave.open(str(wav),'wb') as stream:
            stream.setnchannels(1);stream.setsampwidth(2);stream.setframerate(16000);stream.writeframes(b'\0\0'*16000)
        save(client.run('audio.info',audio=wav),'wav-info.json')
        video=tmp/'fixture.avi'
        writer=cv2.VideoWriter(str(video),cv2.VideoWriter_fourcc(*'MJPG'),10,(160,120))
        if not writer.isOpened():raise RuntimeError('MJPG test codec unavailable')
        for i in range(15):
            frame=np.zeros((120,160,3),dtype=np.uint8);cv2.rectangle(frame,(i*5,40),(i*5+30,75),(255,255,255),-1);writer.write(frame)
        writer.release()
        save(client.run('video.motion',video=video,min_area=20),'motion-fixture.json')
        doc=Document();doc.add_paragraph('خالد سلمان — AlFarouq AI document fixture');doc.save(tmp/'sample.docx')
        book=Workbook();book.active.append(['name','value']);book.active.append(['sample',95]);book.save(tmp/'sample.xlsx')
        c=canvas.Canvas(str(tmp/'sample.pdf'));c.drawString(72,720,'AlFarouq AI extraction fixture');c.save()
        for ext in ('pdf','docx','xlsx'):
            save(client.run('document.read',document=tmp/f'sample.{ext}'),f'{ext}-extraction.json')
    print('Captured real execution artifacts:',len(list(OUT.iterdir())))

if __name__=='__main__':main()
