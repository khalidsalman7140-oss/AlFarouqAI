# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Arabic-first NLP coursework without hidden corpus or model downloads."""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
import re
import unicodedata
from .core import Result, ValidationError, require
from .local import read_csv

HARAKAT=re.compile('[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06ed]')
STOP=set('في من إلى عن على هذا هذه ذلك تلك هو هي هم نحن ان إن أن كان كانت يكون مع او أو ثم و ف ب ل ك ما لا لم لن قد كل بين عند بعد قبل'.split())

def normalize(text,*,alef=True,diacritics=True):
    if not isinstance(text,str):raise ValidationError('text must be a string')
    value=unicodedata.normalize('NFKC',text).replace('\u0640','')
    if diacritics:value=HARAKAT.sub('',value)
    if alef:value=re.sub('[إأآٱ]','ا',value)
    return re.sub(r'\s+',' ',value).strip()

def process(*,text,config,stem=True):
    if not isinstance(text,str) or len(text.encode())>config.max_input_bytes:raise ValidationError('Text must be within Config byte budget')
    value=normalize(text);words=re.findall(r'[^\W_]+',value,re.UNICODE)
    filtered=[w for w in words if w not in STOP]
    stems=[]
    if stem:
        cls=require('nltk.stem.isri','nlp').ISRIStemmer;engine=cls()
        stems=[engine.stem(w) if re.search('[\u0600-\u06ff]',w) else w.casefold() for w in filtered]
    return Result('arabic.process',{'normalized':value,'tokens':words,'filtered_tokens':filtered,'stems':stems,'word_count':len(words),'keywords':Counter(filtered).most_common(15),'sentences':[s.strip() for s in re.split(r'[.!؟?\n]+',text) if s.strip()]},'unicode+nltk.ISRI' if stem else 'stdlib.arabic-normalization',['ISRI is heuristic stemming, not context-aware lemmatization, POS, NER or dialect understanding. Normalization can merge distinct spellings; preserve original source.'])

@dataclass
class TextModel:
    pipeline: object
    report: Result
    def predict(self,texts):
        if not isinstance(texts,list) or not texts or any(not isinstance(t,str) or not t.strip() for t in texts):raise ValidationError('Provide a nonempty list of nonempty text strings')
        values=self.pipeline.predict(texts)
        return Result('nlp.predict',{'rows':[{'text':text,'prediction':str(label)} for text,label in zip(texts,values)]},'sklearn.tfidf-logistic')

def train_text(*,data,text_column,target,config,seed=42):
    require('sklearn','ml')
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score,f1_score,confusion_matrix
    _,rows=read_csv(data,config)
    if text_column==target or any(c not in rows[0] for c in (text_column,target)) or len(rows)<16:raise ValidationError('Distinct existing text/target columns and >=16 rows required')
    if any(not r[text_column].strip() or not r[target].strip() for r in rows):raise ValidationError('Empty texts/labels are not accepted')
    # Exact duplicate texts cannot cross the split or conflict in their labels.
    unique={}
    for row in rows:
        key=normalize(row[text_column]).casefold()
        if key in unique and unique[key][1]!=row[target]:raise ValidationError('Conflicting labels for duplicate normalized text')
        unique[key]=(row[text_column],row[target])
    X,y=zip(*unique.values());counts=Counter(y)
    if len(X)<16 or len(counts)<2 or min(counts.values())<2:raise ValidationError('Need >=16 unique texts, >=2 classes and >=2 texts per class')
    try:xt,xv,yt,yv=train_test_split(list(X),list(y),test_size=.25,random_state=seed,stratify=y)
    except ValueError as exc:raise ValidationError(str(exc)) from exc
    pipeline=Pipeline([('tfidf',TfidfVectorizer(analyzer='char',ngram_range=(2,5),max_features=20000,sublinear_tf=True)),('classifier',LogisticRegression(max_iter=400,random_state=seed))])
    pipeline.fit(xt,yt);pred=pipeline.predict(xv);labels=sorted(counts)
    report=Result('nlp.train',{'classes':labels,'train_rows':len(xt),'test_rows':len(xv),'duplicates_removed':len(rows)-len(unique),'accuracy':float(accuracy_score(yv,pred)),'f1_macro':float(f1_score(yv,pred,average='macro',zero_division=0)),'confusion_matrix':confusion_matrix(yv,pred,labels=labels).tolist(),'rows':[{'actual':a,'prediction':str(b)} for a,b in zip(yv,pred)]},'sklearn.char-tfidf+logistic',['Character n-gram baseline for labeled Arabic/multilingual text. No pretrained sentiment/medical model. Exact duplicates are removed, but author/topic/group leakage still needs domain-aware splitting.'])
    return TextModel(pipeline,report)

def train_report(*,data,text_column,target,config,seed=42):return train_text(data=data,text_column=text_column,target=target,config=config,seed=seed).report

def topics(*,data,text_column,config,n_topics=3,top_words=8):
    require('sklearn','ml')
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    _,rows=read_csv(data,config)
    if text_column not in rows[0] or type(n_topics)is not int or not 2<=n_topics<=10 or not 3<=top_words<=30 or len(rows)<n_topics*2:raise ValidationError('Valid text column, n_topics 2..10 and sufficient rows required')
    vectorizer=CountVectorizer(token_pattern=r'(?u)\b\w\w+\b',max_features=10000)
    try:X=vectorizer.fit_transform([normalize(r[text_column]) for r in rows])
    except ValueError as exc:raise ValidationError('Corpus has no usable vocabulary') from exc
    model=LatentDirichletAllocation(n_components=n_topics,random_state=42,max_iter=10).fit(X);words=vectorizer.get_feature_names_out()
    return Result('nlp.topics',{'rows':[{'topic':i,'words':[str(words[j]) for j in weights.argsort()[-top_words:][::-1]]} for i,weights in enumerate(model.components_)]},'sklearn.LDA',['Unsupervised topics are exploratory, not known ground-truth categories. Arabic morphology/dialects require appropriate preprocessing and evaluation.'])

def similarity(*,texts,query,config,k=5):
    if not isinstance(texts,list) or not texts or len(texts)>10000 or any(not isinstance(t,str) for t in texts) or not isinstance(query,str) or not query.strip() or not 1<=k<=100:raise ValidationError('Bounded text list, nonempty query and k 1..100 required')
    if sum(len(t.encode()) for t in texts)+len(query.encode())>config.max_input_bytes:raise ValidationError('Corpus byte budget exceeded')
    require('sklearn','ml')
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    try:v=TfidfVectorizer(analyzer='char_wb',ngram_range=(2,4)).fit(texts);scores=cosine_similarity(v.transform([query]),v.transform(texts))[0]
    except ValueError as exc:raise ValidationError('No usable text features') from exc
    order=sorted(range(len(texts)),key=lambda i:-scores[i])[:k]
    return Result('nlp.similarity',{'rows':[{'index':i,'text':texts[i],'score':float(scores[i])} for i in order]},'sklearn.lexical-char-tfidf',['Lexical similarity, NOT semantic embeddings. Use rag.search.semantic for trained semantic retrieval.'])
