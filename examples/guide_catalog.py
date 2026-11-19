"""Exact code snippets used by both the complete coding guide and its executor."""
CASES={
 'text.analyze':"result = ai.run('text.analyze', text='الذكاء الاصطناعي يساعد الطلاب. Python helps researchers.')",
 'data.profile':"result = ai.run('data.profile', data=DATA/'numeric.csv')",
 'ml.train':"result = ai.run('ml.train', data=DATA/'numeric.csv', target='target', problem='classification')",
 'image.analyze':"result = ai.run('image.analyze', image=PHOTO)",
 'video.motion':"media_fixtures(DATA, PHOTO)\nresult = ai.run('video.motion', video=DATA/'clip.avi', max_frames=3)",
 'audio.info':"media_fixtures(DATA, PHOTO)\nresult = ai.run('audio.info', audio=DATA/'silence.wav')",
 'speech.transcribe':"ai.run('speech.synthesize', text='Hello world. A speech recognition test.', output=OUT/'speech.wav')\nresult = ai.run('speech.transcribe', audio=OUT/'speech.wav', model_path=str(prepare_model('whisper-tiny')), language='en')",
 'document.read':"result = ai.run('document.read', document=DATA/'note.txt')",
 'code.analyze':"result = ai.run('code.analyze', code='import os\\nos.system(command)\\n')",
 'security.logs':"result = ai.run('security.logs', path=DATA/'auth.log')",
 'iot.analyze':"result = ai.run('iot.analyze', data=DATA/'sensors.csv', column='temperature')",
 'llm.chat':"with model_server() as origin:\n    result = Client(Config(allow_network=True, ollama_url=origin, model='reference-smollm')).run('llm.chat', prompt='What is the capital of France?')",
 'local.generate':"result = ai('Explain Python briefly.', task='local.generate', max_new_tokens=40)",
 'nlp.classify':"result = ai.run('nlp.classify', text='The service was excellent.', labels=['positive','negative'])",
 'code.generate':"result = ai.run('code.generate', prompt='Write a Python function add(a,b).', max_new_tokens=60)",
 'code.repair':"result = ai.run('code.repair', code='def add(a,b)\\n return a+b', error='missing colon', max_new_tokens=60)",
 'code.test':"result = ai.run('code.test', path=DATA/'trusted_tests', consent=True)",
 'document.summarize':"result = ai.run('document.summarize', document=DATA/'note.txt', max_new_tokens=50)",
 'vision.detect':"result = ai.run('vision.detect', image=PHOTO)",
 'vision.classify':"result = ai.run('vision.classify', image=PHOTO, top_k=3)",
 'vision.segment':"result = ai.run('vision.segment', image=PHOTO, output=OUT/'mask.png')",
 'vision.ocr':"media_fixtures(DATA, PHOTO)\nresult = ai.run('vision.ocr', image=DATA/'ocr.png', language='eng')",
 'video.track':"media_fixtures(DATA, PHOTO)\nresult = ai.run('video.track', video=DATA/'clip.avi', max_frames=3)",
 'speech.recognize':"ai.run('speech.synthesize', text='Hello world. A speech recognition test.', output=OUT/'speech.wav')\nresult = ai.run('speech.recognize', audio=OUT/'speech.wav', language='en')",
 'speech.synthesize':"result = ai.run('speech.synthesize', text='Hello world.', output=OUT/'speech.wav', voice='en-us')",
 'deep.train':"result = ai.run('deep.train', data=DATA/'numeric.csv', target='target', problem='classification', epochs=30)",
 'data.forecast':"result = ai.run('data.forecast', data=DATA/'sensors.csv', column='temperature', horizon=3)",
 'data.recommend':"result = ai.run('data.recommend', data=DATA/'ratings.csv', user='u1', user_column='user', item_column='item', rating_column='rating')",
 'security.anomalies':"result = ai.run('security.anomalies', data=DATA/'sensors.csv', columns=['time','temperature'])",
 'rag.index':"result = ai.run('rag.index', document=DATA/'note.txt', store=OUT/'knowledge.sqlite')",
 'rag.search.semantic':"ai.run('rag.index', document=DATA/'note.txt', store=OUT/'knowledge.sqlite')\nresult = ai.run('rag.search.semantic', query='measuring temperature', store=OUT/'knowledge.sqlite')",
 'rag.answer':"ai.run('rag.index', document=DATA/'note.txt', store=OUT/'knowledge.sqlite')\nresult = ai.run('rag.answer', question='What measures heat?', store=OUT/'knowledge.sqlite', min_score=.1)",
 'agents.llm':"result = ai.run('agents.llm', goal='Analyze text statistics.', inputs_by_task={'text.analyze':{'text':'Python helps students.'}})",
 'automation.tick':"scheduler = Scheduler(OUT/'jobs.sqlite')\nscheduler.add('one','text.analyze',{'text':'Hello'},run_at=0)\nscheduler.close()\nresult = ai.run('automation.tick', store=OUT/'jobs.sqlite')",
 'iot.mqtt.publish':"with broker() as port:\n    result = Client(Config(allow_network=True)).run('iot.mqtt.publish', host='127.0.0.1', port=port, topic='demo/readings', message={'temperature':24}, consent=True)",
 'iot.mqtt.read':"with broker() as port:\n    def publish():\n        import time\n        time.sleep(.5)\n        Client(Config(allow_network=True)).run('iot.mqtt.publish', host='127.0.0.1', port=port, topic='demo/readings', message='24', consent=True)\n    thread = threading.Thread(target=publish); thread.start()\n    result = Client(Config(allow_network=True)).run('iot.mqtt.read', host='127.0.0.1', port=port, topic='demo/readings', duration=4)\n    thread.join()",
 'robotics.serial':"import os, select\nmaster, slave = os.openpty()\ndef device_side():\n    if select.select([master],[],[],4)[0]:\n        os.read(master,128); os.write(master,b'PONG')\nthread=threading.Thread(target=device_side); thread.start()\ntry:\n    result=Client(Config(timeout=2)).run('robotics.serial',port=os.ttyname(slave),command='PING',read_bytes=4,consent=True)\n    thread.join()\nfinally:\n    os.close(master); os.close(slave)",
 'arabic.process':"result = ai.ar('يكتب الطلاب دروس اللغة العربية في المدارس')",
 'nlp.train':"model = ai.text_train(data=DATA/'corpus.csv', text_column='text', target='label')\nresult = model.report\nprint(model.predict(['خدمة ممتازة رائعة']).to_dict())",
 'nlp.topics':"result = ai.run('nlp.topics', data=DATA/'corpus.csv', text_column='text', n_topics=2)",
 'nlp.similarity':"result = ai.run('nlp.similarity', texts=['تعلم بايثون','صيانة مضخة'], query='بايثون')",
 'sales.forecast':"result = ai.sales(DATA/'sales.csv', horizon=1)",
 'data.clean':"result = ai.run('data.clean', data=DATA/'appointments.csv')",
 'data.group':"result = ai.run('data.group', data=DATA/'appointments.csv', group_column='department', value_column='waiting_minutes')",
 'privacy.redact':"result = ai.run('privacy.redact', text='Contact person@example.org +967 700 123 456')",
 'finance.reconcile':"result = ai.run('finance.reconcile', left=DATA/'left.csv', right=DATA/'right.csv', key='id', amount_column='amount')",
 'industry.sensors':"result = ai.run('industry.sensors', data=DATA/'sensors.csv', columns=['temperature'], sample_rate=1)",
 'industry.control':"result = ai.run('industry.control', data=DATA/'sensors.csv', baseline=DATA/'baseline.csv', column='temperature')",
 'industry.production':"result = ai.run('industry.production', data=DATA/'production.csv', total_column='total', good_column='good', operating_hours=3)",
 'industry.maintenance':"result = ai.run('industry.maintenance', data=DATA/'numeric.csv', target='target')",
 'industry.defects':"media_fixtures(DATA, PHOTO)\nresult = ai.inspect(DATA/'bad.png', reference=DATA/'good.png', output=OUT/'difference.png')",
 'database.profile':"result = ai.run('database.profile', database=DATA/'factory.sqlite')",
 'code.tests.generate':"result = ai.run('code.tests.generate', code='def add(a,b):\\n    return a+b\\n', max_new_tokens=80)",
 'api.schema':"result = ai.run('api.schema')",
 'onnx.predict':"create_onnx(DATA/'double.onnx')\nresult = ai.run('onnx.predict', model_path=DATA/'double.onnx', inputs={'x':[[2.],[3.]]})",
 'tensorflow.predict':"import tensorflow as tf\nmodel=tf.keras.Sequential([tf.keras.layers.Input(shape=(1,)),tf.keras.layers.Dense(1)])\nimport numpy as np\nmodel.layers[0].set_weights([np.array([[2.]],dtype='float32'),np.array([1.],dtype='float32')])\nmodel.save(DATA/'linear.keras')\nresult = ai.run('tensorflow.predict', model_path=DATA/'linear.keras', inputs=[[2.]])",
 'llm.compatible':"with model_server() as origin:\n    result = Client(Config(allow_network=True)).run('llm.compatible', prompt='What is the capital of France?', endpoint=origin+'/v1', model='reference-smollm')",
 'iot.modbus.read':"with modbus_server() as port:\n    result = Client(Config(allow_network=True)).run('iot.modbus.read', host='127.0.0.1', port=port, address=0, count=2)",
 'document.insights':"result = AI('حلل هذا الملف واستخرج أهم المعلومات', file=DATA/'note.txt')",
 'document.search':"result = ai.run('document.search', document=DATA/'note.txt', query='Python')",
 'ai.search':"result = AI('astar', grid=[[0,0,0],[0,1,0]], start=[0,0], goal=[1,2])",
}
UNVERIFIED={
 'image.objects':'الموصل القديم يتطلب نموذج Transformers محلياً متوافقاً؛ لم يختبر بأوزان فعلية في هذا الإصدار. البديل vision.detect مختبر ولا يحذف المسار القديم.',
 'image.generate':'مسار Stable Diffusion تجريبي غير مختبر بأوزان فعلية ضمن هذه الموارد. لا ندرج مثال توليد تحت وصف مختبر.',
 'video.generate':'مسار CogVideoX يتطلب موارد ونموذجاً مناسباً؛ لم يجر استدلال فعلي، لذلك لا يوجد مثال تشغيل مثبت هنا.'}
MODEL_CASES={'speech.transcribe','llm.chat','local.generate','nlp.classify','code.generate','code.repair','document.summarize','vision.detect','vision.classify','vision.segment','video.track','speech.recognize','rag.index','rag.search.semantic','rag.answer','agents.llm','code.tests.generate','tensorflow.predict','llm.compatible'}
COMMON='''from pathlib import Path
import tempfile, threading
from alfarouqai import AI, Client, Config, Scheduler, prepare_model
from examples.guide_support import make_fixtures, media_fixtures, model_server, broker, modbus_server, create_onnx
ROOT = Path.cwd()  # run from the unpacked AlFarouqAI directory
PHOTO = ROOT/'identity/founder/khalid-salman-original.jpg'
workspace = tempfile.TemporaryDirectory()
DATA, OUT = make_fixtures(workspace.name)
ai = Client()
'''
