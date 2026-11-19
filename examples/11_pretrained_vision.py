import argparse
from alfarouqai import Client, Config
p=argparse.ArgumentParser();p.add_argument('image');p.add_argument('--allow-download',action='store_true');a=p.parse_args()
ai=Client(Config(allow_network=a.allow_download,allow_model_download=a.allow_download))
print(ai.run('vision.detect',image=a.image).to_dict())
print(ai.run('vision.classify',image=a.image).to_dict())
# Segmentation creates a new class-ID mask: ai.run('vision.segment',image=a.image,output='mask.png')
