# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Practical business services with explicit units, periods and baseline limits."""
import re
import statistics
from collections import Counter
from .core import Result, ValidationError, require
from .local import read_csv, finite_number


def infer_column(columns,requested,candidates):
    if requested:
        if requested not in columns:raise ValidationError(f'Unknown column: {requested}')
        return requested
    matches=[c for c in columns if c.casefold().strip() in candidates]
    if len(matches)!=1:raise ValidationError(f'Specify an unambiguous column; candidates found: {matches}')
    return matches[0]


def sales_forecast(*,data,config,date_column=None,value_column=None,horizon=1):
    pd=require('pandas','ml');np=require('numpy','ml');_,rows=read_csv(data,config)
    date_column=infer_column(rows[0],date_column,{'date','التاريخ','month','الشهر'})
    value_column=infer_column(rows[0],value_column,{'sales','المبيعات','revenue','الايرادات','الإيرادات','amount'})
    if date_column==value_column or type(horizon)is not int or not 1<=horizon<=24:raise ValidationError('Distinct date/value columns; horizon 1..24 required')
    parsed=[]
    for row in rows:
        raw=row[date_column]
        if not re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?',raw):raise ValidationError('Dates must be ISO YYYY-MM or YYYY-MM-DD; no locale guessing')
        value=finite_number(row[value_column])
        if value is None:raise ValidationError('Sales values must be finite numbers')
        try:period=pd.Period(raw,freq='M')
        except ValueError as exc:raise ValidationError('Invalid calendar date') from exc
        # Period alone accepts some invalid day strings; validate full dates as well.
        if len(raw)==10:
            import datetime
            try:datetime.date.fromisoformat(raw)
            except ValueError as exc:raise ValidationError('Invalid ISO calendar date') from exc
        parsed.append((period,value))
    aggregated={}
    for month,value in parsed:aggregated[month]=aggregated.get(month,0.)+value
    months=sorted(aggregated)
    if len(months)<6:raise ValidationError('Need at least six distinct historical months')
    expected=list(pd.period_range(months[0],months[-1],freq='M'))
    if months!=expected:raise ValidationError('Historical months contain gaps. Supply complete periods; missing months are not silently treated as zero.')
    y=np.array([aggregated[m] for m in months]);split=max(3,len(y)-max(1,min(3,len(y)//4)))
    coefficient=np.polyfit(np.arange(split),y[:split],1)
    predicted=np.polyval(coefficient,np.arange(split,len(y)));method='linear-trend'
    mae=float(np.abs(predicted-y[split:]).mean())
    # Seasonal baseline is compared only when its holdout can use a full previous year.
    if split>=12:
        seasonal=np.array([y[i-12] for i in range(split,len(y))]);seasonal_mae=float(np.abs(seasonal-y[split:]).mean())
        if seasonal_mae<mae:mae=seasonal_mae;method='seasonal-naive-12'
    future=list(pd.period_range(months[-1]+1,periods=horizon,freq='M'))
    if method=='seasonal-naive-12':
        values=[]
        for i in range(horizon):values.append(float(y[len(y)+i-12]) if i<12 else values[i-12])
    else:
        coefficient=np.polyfit(np.arange(len(y)),y,1);values=np.polyval(coefficient,np.arange(len(y),len(y)+horizon)).tolist()
    return Result('sales.forecast',{'date_column':date_column,'value_column':value_column,'history_months':len(y),'holdout_months':len(y)-split,'holdout_mae':mae,'selected_baseline':method,'history':[{'month':str(m),'total':float(aggregated[m])} for m in months],'rows':[{'month':str(m),'forecast':float(v)} for m,v in zip(future,values)]},'pandas.monthly-aggregation+numpy.temporal-baseline',['Forecasts are estimates, not guaranteed revenue. No calibrated uncertainty interval, promotion/exogenous or causal model. Negative forecasts are not silently clipped.'])


def clean(*,data,config):
    _,rows=read_csv(data,config);seen=set();unique=[]
    for row in rows:
        normalized={k:v.strip() for k,v in row.items()};key=tuple(normalized.items())
        if key not in seen:unique.append(normalized);seen.add(key)
    return Result('data.clean',{'input_rows':len(rows),'duplicates_removed':len(rows)-len(unique),'missing_by_column':{c:sum(not r[c] for r in unique) for c in rows[0]},'rows':unique},'stdlib.explicit-dedup',['Whitespace and exact duplicates only. No arbitrary imputation or destructive in-place overwrite. Review missing-value semantics before modeling.'])


def redact(*,text,config):
    if not isinstance(text,str) or len(text.encode())>config.max_input_bytes:raise ValidationError('Bounded text string required')
    result=text;counts={}
    patterns={'EMAIL':r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b','PHONE':r'(?<!\w)\+?\d[\d ()\-]{7,}\d(?!\w)'}
    for kind,pattern in patterns.items():result,count=re.subn(pattern,'['+kind+']',result);counts[kind]=count
    return Result('privacy.redact',{'text':result,'counts':counts},'stdlib.regex',['Limited email/phone masking, not comprehensive PII anonymization or HIPAA/GDPR compliance. Numbers can be false positives; names/medical identifiers may remain.'])


def reconcile(*,left,right,key,amount_column,config,tolerance=.01):
    if not isinstance(tolerance,(int,float)) or finite_number(tolerance)is None or tolerance<0:raise ValidationError('Nonnegative finite tolerance required')
    _,a=read_csv(left,config);_,b=read_csv(right,config)
    if key==amount_column or any(c not in rows[0] for rows in (a,b) for c in (key,amount_column)):raise ValidationError('Distinct existing key/amount columns required')
    def index(rows):
        result={}
        from decimal import Decimal,InvalidOperation
        for row in rows:
            if not row[key] or row[key] in result:raise ValidationError('Unique nonempty transaction keys required')
            try:v=Decimal(row[amount_column])
            except InvalidOperation as exc:raise ValidationError('Amount must be numeric') from exc
            if not v.is_finite():raise ValidationError('Amount must be finite')
            result[row[key]]=v
        return result
    from decimal import Decimal
    aa,bb=index(a),index(b);rows=[]
    for k in sorted(set(aa)|set(bb)):
        delta=aa[k]-bb[k] if k in aa and k in bb else None
        status='missing-left' if k not in aa else 'missing-right' if k not in bb else 'matched' if abs(delta)<=Decimal(str(tolerance)) else 'amount-mismatch'
        rows.append({'key':k,'status':status,'difference':str(delta) if delta is not None else None})
    return Result('finance.reconcile',{'counts':dict(Counter(r['status'] for r in rows)),'rows':rows},'decimal.keyed-reconciliation',['Operational reconciliation only, not fraud detection, investment advice or automated payment approval. Currency/unit must already match.'])
