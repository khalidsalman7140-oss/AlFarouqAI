# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Actual CPU neural-network training, forecasting, recommendations and anomalies."""
from pathlib import Path
import json
from .core import Result, ValidationError, require
from .local import read_csv, finite_number


def _network(torch,n_inputs,n_outputs,hidden):
    layers=[];current=n_inputs
    for size in hidden:layers.extend([torch.nn.Linear(current,size),torch.nn.ReLU()]);current=size
    layers.append(torch.nn.Linear(current,n_outputs))
    return torch.nn.Sequential(*layers)

class NeuralModel:
    def __init__(self,network,features,labels,problem,mean,scale,hidden,report):
        self.network=network;self.features=features;self.labels=labels;self.problem=problem;self.mean=mean;self.scale=scale;self.hidden=hidden;self.report=report
    def predict(self,rows):
        torch=require('torch','deep');np=require('numpy','ml')
        if not rows or any(set(r)!=set(self.features) for r in rows):raise ValidationError('Prediction features must match training exactly')
        X=np.array([[float(r[c]) for c in self.features] for r in rows],dtype='float32')
        if not np.isfinite(X).all():raise ValidationError('Prediction inputs must be finite')
        with torch.inference_mode():out=self.network(torch.tensor((X-self.mean)/self.scale))
        values=[self.labels[i] for i in out.argmax(1).tolist()] if self.problem=='classification' else out[:,0].tolist()
        return Result('deep.predict',{'rows':[{'prediction':v} for v in values]},'pytorch.cpu-mlp')
    def save(self,directory):
        st=require('safetensors.torch','deep');path=Path(directory);path.mkdir(parents=True,exist_ok=False)
        st.save_file(self.network.state_dict(),str(path/'weights.safetensors'))
        metadata={'features':self.features,'labels':self.labels,'problem':self.problem,'mean':self.mean.tolist(),'scale':self.scale.tolist(),'hidden':self.hidden}
        (path/'model.json').write_text(json.dumps(metadata,ensure_ascii=False),encoding='utf-8')
        return path
    @classmethod
    def load(cls,directory,*,config):
        from .core import input_file
        torch=require('torch','deep');np=require('numpy','ml');st=require('safetensors.torch','deep');path=Path(directory)
        meta=json.loads(input_file(path/'model.json',config).read_text());input_file(path/'weights.safetensors',config)
        if meta['problem'] not in ('classification','regression') or not 1<=len(meta['features'])<=1000 or not 1<=len(meta['hidden'])<=5 or any(type(n)is not int or not 1<=n<=1024 for n in meta['hidden']):raise ValidationError('Invalid neural model metadata')
        mean=np.array(meta['mean'],dtype='float32');scale=np.array(meta['scale'],dtype='float32')
        if mean.shape!=(len(meta['features']),) or scale.shape!=mean.shape or not np.isfinite(mean).all() or not np.isfinite(scale).all() or (scale<=0).any():raise ValidationError('Invalid saved feature scaler')
        net=_network(torch,len(meta['features']),len(meta['labels']) if meta['problem']=='classification' else 1,meta['hidden']);net.load_state_dict(st.load_file(str(path/'weights.safetensors')));net.eval()
        return cls(net,meta['features'],meta['labels'],meta['problem'],mean,scale,meta['hidden'],None)


def train_neural(*,data,target,problem,config,epochs=80,hidden=(32,16),seed=42):
    if problem not in ('classification','regression') or type(epochs)is not int or not 1<=epochs<=500 or not isinstance(hidden,(list,tuple)) or not 1<=len(hidden)<=5 or any(type(h)is not int or not 1<=h<=1024 for h in hidden):raise ValidationError('Explicit problem; epochs 1..500; 1..5 hidden layers of 1..1024 required')
    torch=require('torch','deep');np=require('numpy','ml');require('sklearn','ml')
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score,mean_absolute_error
    torch.set_num_threads(2);torch.manual_seed(seed)
    _,rows=read_csv(data,config)
    if target not in rows[0] or len(rows)<16:raise ValidationError('Target and >=16 rows required')
    features=[k for k in rows[0] if k!=target]
    if not features or len(features)>1000:raise ValidationError('Need 1..1000 features')
    X=np.array([[finite_number(r[c]) for c in features] for r in rows],dtype='float32')
    if not np.isfinite(X).all():raise ValidationError('Neural tabular features must be finite numeric values, no missing values')
    if any(not r[target].strip() for r in rows):raise ValidationError('Missing target labels are not allowed')
    labels=sorted(set(r[target] for r in rows)) if problem=='classification' else []
    if problem=='classification' and (len(labels)<2 or len(labels)>100):raise ValidationError('Need 2..100 classes')
    y=np.array([labels.index(r[target]) if labels else finite_number(r[target]) for r in rows],dtype='int64' if labels else 'float32')
    if not np.isfinite(y).all():raise ValidationError('Targets must be finite')
    try:xt,xv,yt,yv=train_test_split(X,y,test_size=.25,random_state=seed,stratify=y if labels else None)
    except ValueError as exc:raise ValidationError(str(exc)) from exc
    scaler=StandardScaler().fit(xt);xt=torch.tensor(scaler.transform(xt),dtype=torch.float32);xv=torch.tensor(scaler.transform(xv),dtype=torch.float32)
    target_tensor=torch.tensor(yt,dtype=torch.long if labels else torch.float32)
    net=_network(torch,len(features),len(labels) if labels else 1,list(hidden));optimizer=torch.optim.Adam(net.parameters(),lr=.01)
    loss_fn=torch.nn.CrossEntropyLoss() if labels else torch.nn.MSELoss();losses=[]
    net.train()
    for _ in range(epochs):
        optimizer.zero_grad();out=net(xt);loss=loss_fn(out,target_tensor) if labels else loss_fn(out[:,0],target_tensor)
        loss.backward();optimizer.step();losses.append(float(loss.detach()))
    net.eval()
    with torch.inference_mode():pred=net(xv);values=pred.argmax(1).numpy() if labels else pred[:,0].numpy()
    metrics={'accuracy':float(accuracy_score(yv,values))} if labels else {'mae':float(mean_absolute_error(yv,values))}
    report=Result('deep.train',{'problem':problem,'features':features,'hidden_layers':list(hidden),'epochs':epochs,'initial_loss':losses[0],'final_loss':losses[-1],'metrics':metrics,'train_rows':len(yt),'test_rows':len(yv)},'pytorch.cpu-mlp',['Small tabular MLP, not universal deep-learning/finetuning. Random split, not time/group aware.'])
    return NeuralModel(net,features,labels,problem,scaler.mean_.astype('float32'),scaler.scale_.astype('float32'),list(hidden),report)


def neural_report(*,data,target,problem,config,epochs=80,hidden=(32,16),seed=42):
    return train_neural(data=data,target=target,problem=problem,config=config,epochs=epochs,hidden=hidden,seed=seed).report


def forecast(*,data,column,config,horizon=5):
    np=require('numpy','ml');_,rows=read_csv(data,config)
    if column not in rows[0] or type(horizon)is not int or not 1<=horizon<=1000 or len(rows)<10:raise ValidationError('Existing column, >=10 rows and horizon 1..1000 required')
    values=np.array([finite_number(r[column]) for r in rows],dtype=float)
    if not np.isfinite(values).all():raise ValidationError('Forecast series must be finite')
    split=max(5,int(len(values)*.8));trend=np.polyfit(np.arange(split),values[:split],1);held=np.polyval(trend,np.arange(split,len(values)));mae=float(np.abs(held-values[split:]).mean())
    fitted=np.polyfit(np.arange(len(values)),values,1);pred=np.polyval(fitted,np.arange(len(values),len(values)+horizon))
    return Result('data.forecast',{'holdout_mae':mae,'rows':[{'step':i+1,'prediction':float(v)} for i,v in enumerate(pred)]},'numpy.linear-trend',['Linear trend baseline, not seasonal forecasting. Input CSV row order is treated as time. Chronological 80/20 holdout.'])


def recommend(*,data,user,user_column,item_column,rating_column,config,k=5):
    np=require('numpy','ml');_,rows=read_csv(data,config)
    if type(k)is not int or not 1<=k<=100 or any(c not in rows[0] for c in (user_column,item_column,rating_column)):raise ValidationError('Valid columns and k=1..100 required')
    users=sorted(set(r[user_column] for r in rows));items=sorted(set(r[item_column] for r in rows))
    if str(user) not in users or len(users)*len(items)>2_000_000:raise ValidationError('Known user required and dense interaction matrix <=2M cells')
    matrix=np.zeros((len(users),len(items)),dtype=float);seen=set();sums={};counts={}
    for r in rows:
        value=finite_number(r[rating_column])
        if value is None or value<0:raise ValidationError('Ratings must be finite and nonnegative')
        idx=(users.index(r[user_column]),items.index(r[item_column]));sums[idx]=sums.get(idx,0)+value;counts[idx]=counts.get(idx,0)+1
        if r[user_column]==str(user):seen.add(items.index(r[item_column]))
    for idx,value in sums.items():matrix[idx]=value/counts[idx]
    norm=np.linalg.norm(matrix,axis=1);idx=users.index(str(user));similarity=(matrix@matrix[idx])/(norm*max(norm[idx],1e-12)+1e-12);similarity[idx]=0
    score=(similarity@matrix)/(np.abs(similarity).sum()+1e-12)
    ranked=sorted([i for i in range(len(items)) if i not in seen],key=lambda i:-score[i])[:k]
    return Result('data.recommend',{'rows':[{'item':items[i],'score':float(score[i])} for i in ranked]},'numpy.user-cosine-collaborative-filtering',['Small-data collaborative baseline, no cold-start or fairness guarantees.'])


def anomalies(*,data,columns,config,contamination=.1):
    require('sklearn','ml');np=require('numpy','ml')
    from sklearn.ensemble import IsolationForest
    _,rows=read_csv(data,config)
    if not columns or any(c not in rows[0] for c in columns) or not 0<contamination<=.5:raise ValidationError('Valid columns and contamination in (0,.5] required')
    X=np.array([[finite_number(r[c]) for c in columns] for r in rows],dtype=float)
    if not np.isfinite(X).all():raise ValidationError('Finite numeric features required')
    model=IsolationForest(contamination=contamination,random_state=42).fit(X);flags=model.predict(X);scores=model.decision_function(X)
    return Result('security.anomalies',{'rows':[{'row':i,'anomaly':bool(flag==-1),'decision_score':float(score)} for i,(flag,score) in enumerate(zip(flags,scores))]},'sklearn.IsolationForest',['Unsupervised anomalies are not proof of a cyberattack.'])
