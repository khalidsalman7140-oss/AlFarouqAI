"""Run from repository root: python examples/01_quickstart.py"""
from pathlib import Path
from alfarouqai import AI, Client
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'demo-output'
out.mkdir(exist_ok=True)
result = AI('حلل هذا النص', text='الذكاء الاصطناعي يساعد الطلاب. Python helps researchers. Local tools protect privacy.')
print(result.to_dict())
result.export(out / 'text-report.json', overwrite=True)
client = Client()
profile = client.run('data.profile', data=ROOT / 'examples/data/students.csv')
profile.export(out / 'data-report.html', overwrite=True)
print('Reports:', out)
