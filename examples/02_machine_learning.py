"""Requires pip install '.[ml]'; the CSV is a synthetic teaching fixture, not research evidence."""
from pathlib import Path
from alfarouqai import Client
root = Path(__file__).resolve().parents[1]
# Drop score to avoid target-proxy leakage when predicting passed.
import csv, tempfile
with (root/'examples/data/students.csv').open() as f:
    rows = [{k:v for k,v in row.items() if k != 'score'} for row in csv.DictReader(f)]
with tempfile.TemporaryDirectory() as temp:
    data = Path(temp)/'training.csv'
    with data.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    trained = Client().train(data=data, target='passed', problem='classification')
    print(trained.report.to_dict())
    print(trained.predict([{'study_hours':7, 'attendance':90, 'track':'science'}]).to_dict())
    # Export the report, not an unsafe pickle model.
    (root/'demo-output').mkdir(exist_ok=True)
    trained.report.export(root/'demo-output/ml-report.json', overwrite=True)
