import argparse
from alfarouqai import Client,Config,LLMAgent
p=argparse.ArgumentParser();p.add_argument('--allow-download',action='store_true');a=p.parse_args()
ai=Client(Config(allow_network=a.allow_download,allow_model_download=a.allow_download))
print(LLMAgent(client=ai).run('Analyze text statistics.',inputs_by_task={'text.analyze':{'text':'Local AI helps students.'}},max_steps=1).to_dict())
