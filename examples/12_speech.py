import argparse,tempfile
from pathlib import Path
from alfarouqai import Client, Config
p=argparse.ArgumentParser();p.add_argument('--allow-download',action='store_true');a=p.parse_args()
ai=Client(Config(allow_network=a.allow_download,allow_model_download=a.allow_download))
with tempfile.TemporaryDirectory() as temp:
    wav=Path(temp)/'speech.wav'
    print(ai.run('speech.synthesize',text='Hello world. This is a speech test.',output=wav).to_dict())
    print(ai.run('speech.recognize',audio=wav,language='en').to_dict())
