import tempfile
from pathlib import Path
from alfarouqai import Client, Config, NeuralModel
with tempfile.TemporaryDirectory() as temp:
    path=Path(temp)/'numeric.csv'
    path.write_text('x,y,target\n'+'\n'.join(f'{i%10},{i//10},{int(i%10>=5)}' for i in range(100)))
    model=Client().deep_train(data=path,target='target',problem='classification',epochs=40)
    print(model.report.to_dict());model.save(Path(temp)/'network')
    restored=NeuralModel.load(Path(temp)/'network',config=Config())
    print(restored.predict([{'x':8,'y':5}]).to_dict())
