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

import tensorflow as tf
model=tf.keras.Sequential([tf.keras.layers.Input(shape=(1,)),tf.keras.layers.Dense(1)])
import numpy as np
model.layers[0].set_weights([np.array([[2.]],dtype='float32'),np.array([1.],dtype='float32')])
model.save(DATA/'linear.keras')
result = ai.run('tensorflow.predict', model_path=DATA/'linear.keras', inputs=[[2.]])
print(result.to_dict())
