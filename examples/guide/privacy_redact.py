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

result = ai.run('privacy.redact', text='Contact person@example.org +967 700 123 456')
print(result.to_dict())
