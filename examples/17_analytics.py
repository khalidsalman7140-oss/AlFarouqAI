from pathlib import Path
from alfarouqai import Client
root=Path(__file__).resolve().parents[1]
ai=Client()
print(ai.run('data.forecast',data=root/'examples/data/sensors.csv',column='temperature').to_dict())
print(ai.run('security.anomalies',data=root/'examples/data/sensors.csv',columns=['time','temperature']).to_dict())
