"""Opt-in inference: install Ollama and download/review a model separately first.
This example is not run by offline CI and needs your explicit model choice.
python examples/05_ollama.py --model <your-local-model-name>
"""
import argparse
from alfarouqai import Client, Config
parser=argparse.ArgumentParser()
parser.add_argument('--model',required=True)
args=parser.parse_args()
client=Client(Config(model=args.model,allow_network=True))
print(client.run('llm.chat',prompt='اشرح تعلم الآلة باختصار').data['text'])
