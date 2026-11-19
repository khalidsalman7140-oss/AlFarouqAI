from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from pathlib import Path
import tempfile, threading
from alfarouqai import AI, Client, Config, Scheduler, prepare_model
from examples.guide_support import make_fixtures, media_fixtures, model_server, broker, modbus_server, create_onnx
ROOT = Path.cwd()  # run from the unpacked AlFarouqAI directory
PHOTO = ROOT/'identity/founder/khalid-salman-original.jpg'
workspace = tempfile.TemporaryDirectory()
DATA, OUT = make_fixtures(workspace.name)
ai = Client()

with broker() as port:
    def publish():
        import time
        time.sleep(.5)
        Client(Config(allow_network=True)).run('iot.mqtt.publish', host='127.0.0.1', port=port, topic='demo/readings', message='24', consent=True)
    thread = threading.Thread(target=publish); thread.start()
    result = Client(Config(allow_network=True)).run('iot.mqtt.read', host='127.0.0.1', port=port, topic='demo/readings', duration=4)
    thread.join()
print(result.to_dict())
