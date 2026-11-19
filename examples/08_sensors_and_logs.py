from pathlib import Path
from alfarouqai import Client
root=Path(__file__).resolve().parents[1]
client=Client()
print(client.run('iot.analyze',data=root/'examples/data/sensors.csv',column='temperature').to_dict())
print(client.run('security.logs',path=root/'examples/data/auth.log').to_dict())
