# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Explicitly approved MQTT/serial I/O and tests of trusted user projects."""
from pathlib import Path
import ipaddress
import json
import subprocess
import sys
import tempfile
import time
from .core import Result, ConsentRequired, ValidationError, require


def _network(host,config):
    if not config.allow_network:raise ConsentRequired('MQTT requires explicit allow_network=True')
    local=host in ('localhost','127.0.0.1','::1')
    if not local and not config.allow_remote:raise ConsentRequired('Remote MQTT requires allow_remote=True; TLS is enforced')
    return local


def mqtt_publish(*,host,topic,message,config,port=1883,consent=False):
    if consent is not True:raise ConsentRequired('Publishing can trigger physical actuators. Explicit consent=True required; not callable by autonomous default tools.')
    local=_network(host,config)
    if not topic or any(c in topic for c in '#+\0') or len(topic)>500 or not 1<=port<=65535:raise ValidationError('Invalid MQTT topic/port')
    raw=json.dumps(message,ensure_ascii=False) if not isinstance(message,str) else message
    if len(raw.encode())>100_000:raise ValidationError('MQTT message too large')
    mqtt=require('paho.mqtt.client','iot')
    client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if not local:client.tls_set()
    try:
        client.connect(host,port,keepalive=20);client.loop_start()
        info=client.publish(topic,raw,qos=1,retain=False);info.wait_for_publish(timeout=config.timeout)
        if not info.is_published():raise ValidationError('MQTT publish was not acknowledged')
    finally:client.disconnect();client.loop_stop()
    return Result('iot.mqtt.publish',{'topic':topic,'bytes':len(raw.encode()),'acknowledged':True},'paho-mqtt.qos1',['Broker acknowledgement is NOT evidence that a physical device acted successfully.'])


def mqtt_read(*,host,topic,config,port=1883,max_messages=1,duration=3):
    local=_network(host,config)
    if not topic or len(topic)>500 or '\0' in topic or not 1<=port<=65535 or type(max_messages)is not int or not 1<=max_messages<=100 or not 0<float(duration)<=30:raise ValidationError('Invalid MQTT read parameters')
    mqtt=require('paho.mqtt.client','iot');client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2);rows=[]
    def connected(c,u,flags,code,properties):
        if code==0:c.subscribe(topic,qos=1)
    def message(c,u,msg):
        if len(msg.payload)<=100_000 and len(rows)<max_messages:rows.append({'topic':msg.topic,'payload':msg.payload.decode('utf-8',errors='replace'),'qos':msg.qos})
    client.on_connect=connected;client.on_message=message
    if not local:client.tls_set()
    try:
        client.connect(host,port,keepalive=20);client.loop_start();deadline=time.monotonic()+float(duration)
        while len(rows)<max_messages and time.monotonic()<deadline:time.sleep(.02)
    finally:client.disconnect();client.loop_stop()
    return Result('iot.mqtt.read',{'rows':rows,'timed_out':len(rows)<max_messages},'paho-mqtt.subscribe',['Only messages actually received are returned. Local broker tests do not prove physical sensor integration.'])


def serial_exchange(*,port,config,baudrate=9600,read_bytes=128,command=None,consent=False):
    if consent is not True:raise ConsentRequired('Serial I/O can control a robot or device. Review wiring/protocol and explicitly pass consent=True.')
    if '://' in port or type(read_bytes)is not int or not 1<=read_bytes<=4096 or baudrate not in (1200,2400,4800,9600,19200,38400,57600,115200):raise ValidationError('Local serial port and bounded read/approved baudrate required')
    if command is not None and (not isinstance(command,str) or len(command.encode())>1024):raise ValidationError('Command must be a string <=1024 bytes')
    serial=require('serial','iot')
    with serial.Serial(port,baudrate=baudrate,timeout=min(config.timeout,5),write_timeout=min(config.timeout,5)) as stream:
        count=stream.write(command.encode()) if command is not None else 0
        stream.flush();received=stream.read(read_bytes)
    return Result('robotics.serial',{'port':port,'written_bytes':count,'received_hex':received.hex(),'text':received.decode('utf-8',errors='replace')},'pyserial.local-port',['Raw serial transport only, not robot kinematics/navigation or safety certification. A successful write does not prove an actuator state.'])


def code_test(*,path,config,consent=False):
    if consent is not True:raise ConsentRequired('Testing executes user Python with OS privileges. Only trusted projects, explicit consent=True, and a separate disposable environment; this is NOT a security sandbox.')
    root=Path(path).resolve()
    if not root.is_dir():raise ValidationError('Test project directory does not exist')
    tests=list(root.glob('test*.py'))
    if not tests or len(tests)>100:raise ValidationError('Need 1..100 top-level unittest test*.py files')
    with tempfile.TemporaryFile(mode='w+',encoding='utf-8') as output:
        try:
            p=subprocess.run([sys.executable,'-I','-m','unittest','discover','-s',str(root),'-p','test*.py','-v'],cwd=root,stdout=output,stderr=subprocess.STDOUT,timeout=min(config.timeout,120),shell=False)
            timed_out=False;returncode=p.returncode
        except subprocess.TimeoutExpired:timed_out=True;returncode=None
        output.seek(0,2);size=output.tell();output.seek(max(0,size-16000));log=output.read()
    return Result('code.test',{'returncode':returncode,'passed':returncode==0 and not timed_out,'timed_out':timed_out,'log':log},'python.unittest.subprocess',['Trusted-code runner only. Isolation flag and timeout do NOT block network/filesystem access or child-process side effects.'])
