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

import os, select
master, slave = os.openpty()
def device_side():
    if select.select([master],[],[],4)[0]:
        os.read(master,128); os.write(master,b'PONG')
thread=threading.Thread(target=device_side); thread.start()
try:
    result=Client(Config(timeout=2)).run('robotics.serial',port=os.ttyname(slave),command='PING',read_bytes=4,consent=True)
    thread.join()
finally:
    os.close(master); os.close(slave)
print(result.to_dict())
