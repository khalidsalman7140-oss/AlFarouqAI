"""Reproducible TEACHING fixtures and local reference servers, not production data.
No server starts on import. Used to execute the exact coding-guide examples.
"""
from pathlib import Path
import csv,contextlib,json,os,socket,subprocess,sys,tempfile,threading,time


def make_fixtures(root):
    root=Path(root);data=root/'data';out=root/'outputs';data.mkdir(parents=True,exist_ok=True);out.mkdir(exist_ok=True)
    def write(name,header,rows):
        with (data/name).open('w',newline='',encoding='utf-8') as stream:
            w=csv.writer(stream);w.writerow(header);w.writerows(rows)
    write('numeric.csv',['x','y','target'],[(i%10,i//10,int(i%10>=5)) for i in range(100)])
    write('sales.csv',['date','sales'],[(f'{2024+i//12}-{i%12+1:02d}-01',100+10*i) for i in range(24)])
    write('sensors.csv',['time','temperature'],[(i,21+i%3 if i!=25 else 80) for i in range(40)])
    write('baseline.csv',['time','temperature'],[(i,21+i%3) for i in range(40)])
    write('production.csv',['total','good'],[(100,95),(200,190)])
    write('corpus.csv',['text','label'],[(f'خدمة ممتازة رائعة وسريعة تجربة رقم {i}','positive') for i in range(24)]+[(f'خدمة سيئة بطيئة ومزعجة تجربة رقم {i}','negative') for i in range(24)])
    write('ratings.csv',['user','item','rating'],[('u1','a',5),('u1','b',4),('u2','a',5),('u2','b',4),('u2','c',5)])
    write('left.csv',['id','amount'],[('a','.30'),('b','2')]);write('right.csv',['id','amount'],[('a','.3'),('c','4')])
    write('appointments.csv',['department','waiting_minutes'],[('Lab',10),('Clinic',20),('Lab',12)])
    (data/'note.txt').write_text('AlFarouq AI helps students use Python. Temperature sensors measure heat.\nخالد سلمان مؤسس المشروع. التاريخ 2026-11-16.',encoding='utf-8')
    (data/'auth.log').write_text('Failed password for root from 192.0.2.10 port 1000\n')
    trusted=data/'trusted_tests';trusted.mkdir(exist_ok=True);(trusted/'test_math.py').write_text('import unittest\nclass T(unittest.TestCase):\n def test_add(self):self.assertEqual(1+1,2)\n')
    import sqlite3
    db=sqlite3.connect(data/'factory.sqlite');db.execute('CREATE TABLE IF NOT EXISTS readings(id INTEGER PRIMARY KEY,value REAL)');db.execute('INSERT OR REPLACE INTO readings VALUES(1,2)');db.commit();db.close()
    return data,out


def media_fixtures(data,photo):
    import cv2,numpy as np,wave
    from PIL import Image,ImageDraw,ImageFont
    data=Path(data)
    good=np.full((128,128,3),255,dtype=np.uint8);bad=good.copy();cv2.rectangle(bad,(35,45),(65,75),(0,0,0),-1)
    cv2.imwrite(str(data/'good.png'),good);cv2.imwrite(str(data/'bad.png'),bad)
    frame=cv2.resize(cv2.imread(str(photo)),(360,800));video=cv2.VideoWriter(str(data/'clip.avi'),cv2.VideoWriter_fourcc(*'MJPG'),5,(360,800))
    if not video.isOpened():raise RuntimeError('MJPG verification codec unavailable')
    for _ in range(3):video.write(frame)
    video.release()
    with wave.open(str(data/'silence.wav'),'wb') as stream:stream.setnchannels(1);stream.setsampwidth(2);stream.setframerate(16000);stream.writeframes(b'\0\0'*16000)
    image=Image.new('RGB',(800,160),'white');draw=ImageDraw.Draw(image);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',42);draw.text((20,40),'ALFAROUQ AI 2026',font=font,fill='black');image.save(data/'ocr.png')


def create_onnx(path):
    from onnx import helper,TensorProto,save
    x=helper.make_tensor_value_info('x',TensorProto.FLOAT,[None,1]);y=helper.make_tensor_value_info('y',TensorProto.FLOAT,[None,1]);c=helper.make_tensor('two',TensorProto.FLOAT,[1],[2.])
    m=helper.make_model(helper.make_graph([helper.make_node('Mul',['x','two'],['y'])],'double',[x],[y],[c]),opset_imports=[helper.make_opsetid('',17)]);m.ir_version=9;save(m,path)


@contextlib.contextmanager
def model_server():
    """Real local trained inference, HTTP-compatible reference, NOT Ollama/vLLM software."""
    from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
    from alfarouqai import Config
    from alfarouqai.language import LocalLanguageModel
    with LocalLanguageModel(config=Config()) as lm:
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                request=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                content=lm.generate(request['messages'][-1]['content'],max_new_tokens=32).data['text']
                body={'model':'reference-smollm','message':{'content':content},'done':True} if self.path=='/api/chat' else {'model':'reference-smollm','choices':[{'message':{'content':content}}]}
                raw=json.dumps(body).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
            def log_message(self,*args):pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:yield f'http://127.0.0.1:{server.server_port}'
        finally:server.shutdown();server.server_close();thread.join()


@contextlib.contextmanager
def broker():
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    with tempfile.TemporaryDirectory() as tmp:
        conf=Path(tmp)/'broker.conf';conf.write_text(f'listener {port} 127.0.0.1\nallow_anonymous true\npersistence false\n')
        p=subprocess.Popen(['mosquitto','-c',str(conf)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(100):
                try:
                    with socket.create_connection(('127.0.0.1',port),timeout=.1):break
                except OSError:time.sleep(.02)
            yield port
        finally:p.terminate();p.wait(timeout=5)


@contextlib.contextmanager
def modbus_server():
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    with tempfile.TemporaryDirectory() as tmp:
        f=Path(tmp)/'server.py';f.write_text('from pymodbus.datastore import ModbusDeviceContext,ModbusSequentialDataBlock,ModbusServerContext\nfrom pymodbus.server import StartTcpServer\nc=ModbusServerContext(devices=ModbusDeviceContext(hr=ModbusSequentialDataBlock(1,[10,20,30,40])),single=True)\nStartTcpServer(c,address=("127.0.0.1",'+str(port)+'))\n')
        p=subprocess.Popen([sys.executable,str(f)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(100):
                try:
                    with socket.create_connection(('127.0.0.1',port),timeout=.1):break
                except OSError:time.sleep(.02)
            yield port
        finally:p.terminate();p.wait(timeout=5)
