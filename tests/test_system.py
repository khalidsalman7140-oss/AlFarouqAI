"""Actual OS engines/protocol transport, not mocks or physical-device claims."""
import os
import select
import shutil
import socket
import subprocess
import threading
import time
from pathlib import Path
import pytest
from alfarouqai import Client, Config
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/v0.2-model-results'


@pytest.mark.system
@pytest.mark.skipif(not shutil.which('tesseract'),reason='Tesseract executable not installed')
def test_real_tesseract_eng_and_arabic(tmp_path):
    PIL=pytest.importorskip('PIL.Image');Draw=pytest.importorskip('PIL.ImageDraw');Font=pytest.importorskip('PIL.ImageFont')
    image=PIL.new('RGB',(1000,200),'white');draw=Draw.Draw(image)
    font=Font.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',50)
    draw.text((30,50),'ALFAROUQ AI 2026',font=font,fill='black')
    path=tmp_path/'ocr.png';image.save(path)
    r=Client().run('vision.ocr',image=path)
    assert 'ALFAROUQ' in r.data['text'] and '2026' in r.data['text']
    OUT.mkdir(parents=True,exist_ok=True);r.export(OUT/'ocr-english.json',overwrite=True)
    languages=subprocess.run(['tesseract','--list-langs'],capture_output=True,text=True).stdout
    if 'ara' in languages:
        image=PIL.new('RGB',(1000,200),'white');Draw.Draw(image).text((30,50),'الذكاء الاصطناعي يساعد الطلاب',font=font,fill='black',direction='rtl',language='ar')
        path=tmp_path/'arabic.png';image.save(path)
        r=Client().run('vision.ocr',image=path,language='ara')
        assert r.data['text'].strip();r.export(OUT/'ocr-arabic.json',overwrite=True)


@pytest.mark.system
@pytest.mark.skipif(not shutil.which('mosquitto'),reason='Optional Mosquitto broker not installed')
def test_actual_mqtt_broker_roundtrip(tmp_path):
    pytest.importorskip('paho.mqtt.client')
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    config=tmp_path/'mosquitto.conf';config.write_text(f'listener {port} 127.0.0.1\nallow_anonymous true\npersistence false\n')
    proc=subprocess.Popen(['mosquitto','-c',str(config)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    result={};errors=[]
    try:
        for _ in range(100):
            try:
                with socket.create_connection(('127.0.0.1',port),timeout=.1):break
            except OSError:time.sleep(.03)
        client=Client(Config(allow_network=True,timeout=5))
        def reader():
            try:result['read']=client.run('iot.mqtt.read',host='127.0.0.1',port=port,topic='alfarouq/test',duration=5)
            except Exception as exc:errors.append(exc)
        thread=threading.Thread(target=reader);thread.start();time.sleep(.5)
        published=client.run('iot.mqtt.publish',host='127.0.0.1',port=port,topic='alfarouq/test',message={'temperature':24},consent=True)
        thread.join(8);assert not thread.is_alive() and not errors
        assert published.data['acknowledged'] and '24' in result['read'].data['rows'][0]['payload']
        OUT.mkdir(parents=True,exist_ok=True);published.export(OUT/'mqtt-publish.json',overwrite=True);result['read'].export(OUT/'mqtt-read.json',overwrite=True)
    finally:proc.terminate();proc.wait(timeout=5)


@pytest.mark.system
@pytest.mark.skipif(not hasattr(os,'openpty'),reason='POSIX pseudo-terminal transport test')
def test_actual_serial_kernel_pty_roundtrip():
    pytest.importorskip('serial')
    master,slave=os.openpty();path=os.ttyname(slave);received=[]
    def device_side():
        if select.select([master],[],[],5)[0]:
            received.append(os.read(master,128));os.write(master,b'PONG')
    thread=threading.Thread(target=device_side);thread.start()
    try:
        r=Client(Config(timeout=3)).run('robotics.serial',port=path,command='PING',read_bytes=4,consent=True)
        thread.join(6);assert received==[b'PING'] and r.data['text']=='PONG'
        OUT.mkdir(parents=True,exist_ok=True);r.warnings.append('Verification used a real kernel pseudo-terminal, NOT a physical sensor/robot.');r.export(OUT/'serial-pty.json',overwrite=True)
    finally:os.close(master);os.close(slave)
