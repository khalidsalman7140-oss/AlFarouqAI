# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Value-oriented service additions; original capability names remain stable."""
import re
from .core import Capability,Result
from . import arabic,business,industry,developer,engines,industrial_io,coursework


def document_insights(*,document,config):
    from .documents import document_read
    from .local import text_analyze
    doc=document_read(document=document,config=config);text=doc.data['text'];analysis=text_analyze(text=text,config=config)
    return Result('document.insights',{'characters':len(text),'words':analysis.data['words'],'summary':analysis.data['extractive_summary'],'keywords':analysis.data['keywords'],'dates_found':sorted(set(re.findall(r'\b\d{4}-\d{2}-\d{2}\b',text))),'emails_found':sorted(set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',text)))},doc.backend+'+extractive-statistics',doc.warnings+['Extractive information only, not legal/clinical interpretation or automatic scanned-PDF OCR.'],doc.provenance)


def document_search(*,document,query,config,k=3):
    from .documents import document_read,KnowledgeBase
    doc=document_read(document=document,config=config);kb=KnowledgeBase();kb.add(doc.data['text'],source=str(document));result=kb.search(query,k=k);result.task='document.search';return result


def group_data(*,data,group_column,config,value_column=None):
    from .local import read_csv,finite_number
    from .core import ValidationError
    _,rows=read_csv(data,config)
    if group_column not in rows[0] or (value_column is not None and value_column not in rows[0]):raise ValidationError('Existing grouping/value columns required')
    groups={}
    for row in rows:
        key=row[group_column];item=groups.setdefault(key,{'group':key,'count':0,'total':0.});item['count']+=1
        if value_column:
            value=finite_number(row[value_column])
            if value is None:raise ValidationError('Finite numeric value column required')
            item['total']+=value
    result=[]
    for key in sorted(groups):
        item=groups[key]
        if value_column:item['mean']=item['total']/item['count']
        else:item.pop('total')
        result.append(item)
    return Result('data.group',{'rows':result},'stdlib.grouped-aggregation',['Operational grouping only; use appropriate anonymization and authorization for patient/customer records. No clinical or credit decisions.'])


def register_services(registry):
    definitions=[
      ('arabic.process',arabic.process,'Normalize, tokenize and optionally stem Arabic text',('text',),'nlp'),
      ('nlp.train',arabic.train_report,'Train and evaluate a labeled Arabic/multilingual text classifier',('data','text_column','target'),'ml'),
      ('nlp.topics',arabic.topics,'Discover exploratory corpus topics using LDA',('data','text_column'),'ml'),
      ('nlp.similarity',arabic.similarity,'Rank text passages by lexical character TF-IDF similarity',('texts','query'),'ml'),
      ('sales.forecast',business.sales_forecast,'Aggregate calendar months and forecast sales using temporal baselines',('data',),'ml'),
      ('data.clean',business.clean,'Trim fields and remove exact duplicate CSV rows for review',('data',),None),
      ('data.group',group_data,'Aggregate operational records by an explicit grouping column',('data','group_column'),None),
      ('privacy.redact',business.redact,'Mask email/phone patterns without pretending full anonymization',('text',),None),
      ('finance.reconcile',business.reconcile,'Reconcile two keyed ledgers using exact decimal amounts',('left','right','key','amount_column'),None),
      ('industry.sensors',industry.sensors,'Extract vibration/sensor statistics and explicitly sampled spectra',('data','columns'),'ml'),
      ('industry.control',industry.control,'Screen measurements against separate baseline control limits',('data','column','baseline'),None),
      ('industry.production',industry.production,'Compute production yield, rejects and optional hourly throughput',('data','total_column','good_column'),None),
      ('industry.maintenance',industry.maintenance,'Evaluate a supervised maintenance-label classifier on historical data',('data','target'),'ml'),
      ('industry.defects',industry.defects,'Locate aligned-reference image differences for quality screening',('image','reference'),'vision'),
      ('database.profile',developer.database_profile,'Read SQLite schema and row counts without modifying the database',('database',),None),
      ('code.tests.generate',developer.tests_generate,'Generate untrusted unittest suggestions with syntax diagnostics',('code',),'local'),
      ('api.schema',api_schema,'Build the authenticated text API OpenAPI schema',(),'api'),
      ('onnx.predict',engines.onnx_predict,'Run reviewed local ONNX tensors with the CPU runtime',('model_path','inputs'),'onnx'),
      ('tensorflow.predict',engines.tensorflow_predict,'Run a reviewed local single-output Keras model',('model_path','inputs'),'tensorflow'),
      ('llm.compatible',engines.compatible_chat,'Call an explicitly approved OpenAI-compatible optional inference endpoint',('prompt','endpoint','model'),None),
      ('iot.modbus.read',industrial_io.modbus_read,'Read bounded holding registers from an approved local gateway',('host','address','count'),'industrial'),
      ('document.insights',document_insights,'Extract text, keywords, dates and an extractive summary from a file',('document',),'documents'),
      ('document.search',document_search,'Search document passages lexically with source references',('document','query'),'documents'),
      ('ai.search',coursework.search,'Solve a bounded unit-cost grid shortest path with A-star',('grid','start','goal'),None),
    ]
    for name,handler,description,required,extra in definitions:registry.register(Capability(name,handler,description,required,extra))


def api_schema(*,config):
    from .api import schema
    return schema(config=config)
