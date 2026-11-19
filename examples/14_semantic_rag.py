import argparse,tempfile
from pathlib import Path
from alfarouqai import VectorStore,Config
p=argparse.ArgumentParser();p.add_argument('--allow-download',action='store_true');a=p.parse_args()
config=Config(allow_network=a.allow_download,allow_model_download=a.allow_download)
with tempfile.TemporaryDirectory() as temp:
    with VectorStore(Path(temp)/'knowledge.sqlite',config=config) as db:
        db.add('المستشعر يقيس درجة الحرارة.',source='lesson')
        print(db.search('measuring temperature').to_dict())
        print(db.answer('What measures temperature?',min_score=.1).to_dict())
