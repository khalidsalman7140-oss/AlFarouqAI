"""Capture real 0.2 teaching-model artifacts. Requires deep/ml/persistence extras.
No network or pretrained model download; all generated teaching data are explicit.
"""
from pathlib import Path
import csv
from alfarouqai import Client

ROOT=Path(__file__).resolve().parents[1]

def main():
    out=ROOT/'reports/v0.2-learning-results';out.mkdir(parents=True,exist_ok=True)
    data=ROOT/'examples/data/neural.csv'
    with data.open('w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['x','y','target'])
        for i in range(100):writer.writerow([i%10,i//10,int(i%10>=5)])
    ratings=ROOT/'examples/data/ratings.csv'
    ratings.write_text('user,item,rating\nu1,a,5\nu1,b,4\nu2,a,5\nu2,b,4\nu2,c,5\nu3,d,5\n')
    ai=Client();model=ai.deep_train(data=data,target='target',problem='classification',epochs=40)
    model.report.warnings.append('Synthetic teaching fixture, not evidence of real-world accuracy.')
    model.report.export(out/'neural-training.json',overwrite=True)
    model.predict([{'x':8,'y':5}]).export(out/'neural-predictions.csv',overwrite=True)
    model.save(out/'neural-model')
    for task,inputs,name in [
        ('data.forecast',{'data':ROOT/'examples/data/sensors.csv','column':'temperature'},'forecast.json'),
        ('data.recommend',{'data':ratings,'user':'u1','user_column':'user','item_column':'item','rating_column':'rating'},'recommendations.json'),
        ('security.anomalies',{'data':ROOT/'examples/data/sensors.csv','columns':['time','temperature']},'anomalies.json')]:
        ai.run(task,**inputs).export(out/name,overwrite=True)
    print('Actual training/prediction/persistence/analytics captured:',out)

if __name__=='__main__':main()
