"""Read a user file, without uploading it. Binary Office/PDF require documents extra."""
import argparse
from alfarouqai import Client
parser=argparse.ArgumentParser(); parser.add_argument('document'); args=parser.parse_args()
result=Client().run('document.read',document=args.document)
print(result.data['text'])
