"""python examples/06_vision.py /path/to/image.jpg — requires vision extra."""
import argparse
from alfarouqai import Client
p=argparse.ArgumentParser(); p.add_argument('image'); args=p.parse_args()
print(Client().run('image.analyze',image=args.image).to_dict())
# General objects require an explicit reviewed local model, not Haar faces:
# client.run('image.objects',image=args.image,model_path='/path/to/model')
