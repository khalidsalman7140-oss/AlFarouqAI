"""Requires local extra and reviewed model cache. --allow-download explicitly opts in."""
import argparse
from alfarouqai import Client, Config
p=argparse.ArgumentParser();p.add_argument('--allow-download',action='store_true');a=p.parse_args()
ai=Client(Config(allow_network=a.allow_download,allow_model_download=a.allow_download))
print(ai.run('local.generate',prompt='What is the capital of France?',max_new_tokens=40).to_dict())
