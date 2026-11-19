"""Real optional engines; external-server compatibility is not a deployment claim."""
import json,os,threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import pytest
from alfarouqai import Client,Config,ConsentRequired


@pytest.mark.optional
def test_actual_onnx_runtime(tmp_path):
    onnx=pytest.importorskip('onnx');pytest.importorskip('onnxruntime')
    from onnx import helper,TensorProto
    x=helper.make_tensor_value_info('x',TensorProto.FLOAT,[None,1]);y=helper.make_tensor_value_info('y',TensorProto.FLOAT,[None,1])
    two=helper.make_tensor('two',TensorProto.FLOAT,[1],[2.]);node=helper.make_node('Mul',['x','two'],['y'])
    model=helper.make_model(helper.make_graph([node],'double',[x],[y],[two]),opset_imports=[helper.make_opsetid('',17)]);model.ir_version=9
    path=tmp_path/'double.onnx';onnx.save(model,path)
    r=Client().run('onnx.predict',model_path=path,inputs={'x':[[2.],[3.]]})
    assert r.data['outputs']['y']==[[4.],[6.]]


@pytest.mark.model
@pytest.mark.skipif(os.environ.get('ALFAROUQ_RUN_MODELS')!='1',reason='Explicit heavy-engine test approval required')
def test_actual_tensorflow_training_save_and_inference(tmp_path):
    tf=pytest.importorskip('tensorflow')
    tf.config.threading.set_intra_op_parallelism_threads(1);tf.config.threading.set_inter_op_parallelism_threads(1)
    tf.random.set_seed(42)
    model=tf.keras.Sequential([tf.keras.layers.Input(shape=(1,)),tf.keras.layers.Dense(1,kernel_initializer='zeros',bias_initializer='zeros')])
    optimizer=tf.keras.optimizers.SGD(.05);x=tf.constant([[0.],[1.],[2.],[3.]]);y=2*x+1
    for _ in range(200):
        with tf.GradientTape() as tape:loss=tf.reduce_mean((model(x)-y)**2)
        optimizer.apply_gradients(zip(tape.gradient(loss,model.trainable_variables),model.trainable_variables))
    path=tmp_path/'linear.keras';model.save(path)
    result=Client().run('tensorflow.predict',model_path=path,inputs=[[2.]])
    assert abs(result.data['outputs'][0][0]-5)<.1


@pytest.mark.model
@pytest.mark.skipif(os.environ.get('ALFAROUQ_RUN_MODELS')!='1',reason='Actual local LLM cache required')
def test_real_model_over_compatible_and_ollama_protocols():
    from alfarouqai.language import LocalLanguageModel
    with LocalLanguageModel(config=Config()) as lm:
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                text=lm.generate(payload['messages'][-1]['content'],max_new_tokens=24).data['text']
                response={'model':'reference-smollm','message':{'content':text},'done':True} if self.path=='/api/chat' else {'model':'reference-smollm','choices':[{'message':{'content':text}}]}
                raw=json.dumps(response).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
            def log_message(self,*args):pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            origin=f'http://127.0.0.1:{server.server_port}';ai=Client(Config(allow_network=True,ollama_url=origin,model='reference-smollm'))
            result=ai.run('llm.compatible',prompt='What is the capital of France?',endpoint=origin+'/v1',model='reference-smollm')
            assert 'Paris' in result.data['text']
            result=ai.run('llm.chat',prompt='What is the capital of France?');assert 'Paris' in result.data['text']
        finally:server.shutdown();server.server_close();thread.join()
    # This is real model+HTTP inference, NOT an installed vLLM/Ollama software claim.


@pytest.mark.model
@pytest.mark.skipif(os.environ.get('ALFAROUQ_RUN_MODELS')!='1',reason='Actual local LLM cache required')
def test_test_generation_actual_model():
    r=Client().run('code.tests.generate',code='def add(a,b):\n    return a+b\n',max_new_tokens=90)
    assert r.data['text'] and isinstance(r.data['syntax_valid'],bool)


@pytest.mark.system
def test_modbus_consent_and_real_local_server(tmp_path):
    pytest.importorskip('pymodbus');import socket,subprocess,sys,time
    with pytest.raises(ConsentRequired):Client().run('iot.modbus.read',host='127.0.0.1',address=0,count=1)
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    script=tmp_path/'server.py';script.write_text('from pymodbus.datastore import ModbusDeviceContext,ModbusSequentialDataBlock,ModbusServerContext\nfrom pymodbus.server import StartTcpServer\ncontext=ModbusServerContext(devices=ModbusDeviceContext(hr=ModbusSequentialDataBlock(1,[10,20,30,40,50,60])),single=True)\nStartTcpServer(context,address=("127.0.0.1",'+str(port)+'))\n')
    p=subprocess.Popen([sys.executable,str(script)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(100):
            try:
                with socket.create_connection(('127.0.0.1',port),timeout=.1):break
            except OSError:time.sleep(.03)
        r=Client(Config(allow_network=True)).run('iot.modbus.read',host='127.0.0.1',port=port,address=0,count=2)
        assert len(r.data['registers'])==2 and all(isinstance(x,int) for x in r.data['registers'])
    finally:p.terminate();p.wait(timeout=5)
