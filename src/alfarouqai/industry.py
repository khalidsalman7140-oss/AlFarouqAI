# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Industrial decision-support baselines; never imply equipment safety certification."""
import math
import statistics
from pathlib import Path
from .core import Result,ValidationError,require,fingerprint
from .local import read_csv,finite_number


def sensors(*,data,columns,config,sample_rate=None):
    np=require('numpy','ml');_,rows=read_csv(data,config)
    if not isinstance(columns,list) or not columns or any(c not in rows[0] for c in columns):raise ValidationError('Explicit existing numeric sensor columns required')
    if sample_rate is not None and (finite_number(sample_rate)is None or sample_rate<=0):raise ValidationError('sample_rate must be finite Hz > 0')
    result=[]
    for col in columns:
        x=np.array([finite_number(r[col]) for r in rows],dtype=float)
        if len(x)<4 or not np.isfinite(x).all():raise ValidationError('Need >=4 finite observations per sensor')
        std=float(x.std());rms=float(np.sqrt(np.mean(x*x)));centered=x-x.mean()
        item={'sensor':col,'samples':len(x),'mean':float(x.mean()),'std':std,'rms':rms,'peak_to_peak':float(np.ptp(x)),'crest_factor':float(np.abs(x).max()/rms) if rms else 0.,'kurtosis_non_excess':float(np.mean(centered**4)/std**4) if std else 0.}
        if sample_rate is not None:
            spectrum=np.abs(np.fft.rfft(centered));frequencies=np.fft.rfftfreq(len(x),d=1./sample_rate)
            item['dominant_frequency_hz']=float(frequencies[1+int(spectrum[1:].argmax())]) if np.any(spectrum[1:]>1e-10) else 0.
        result.append(item)
    return Result('industry.sensors',{'rows':result},'numpy.signal-features',['Frequency estimates assume uniform sampling at the explicitly supplied Hz. Features alone do not diagnose bearing faults or predict remaining useful life.'])


def control(*,data,column,baseline,config,sigma=3.):
    _,current=read_csv(data,config);_,reference=read_csv(baseline,config)
    if column not in current[0] or column not in reference[0] or finite_number(sigma)is None or not 1<=sigma<=6:raise ValidationError('Existing column in current and baseline, sigma 1..6 required')
    a=[finite_number(r[column]) for r in reference];b=[finite_number(r[column]) for r in current]
    if len(a)<10 or any(v is None for v in a+b):raise ValidationError('Baseline >=10 finite values and finite current values required')
    mean=statistics.mean(a);std=statistics.stdev(a)
    if std==0:raise ValidationError('Zero-variance baseline cannot estimate statistical control limits')
    lower,upper=mean-sigma*std,mean+sigma*std
    return Result('industry.control',{'mean':mean,'baseline_std':std,'lower_control_limit':lower,'upper_control_limit':upper,'rows':[{'row':i,'value':v,'out_of_control':v<lower or v>upper} for i,v in enumerate(b)]},'statistics.phase-II-shewhart',['Baseline-estimated statistical control limits are NOT engineering specification limits. Check baseline stability, autocorrelation, stationarity and sampling before action.'])


def production(*,data,total_column,good_column,config,operating_hours=None):
    _,rows=read_csv(data,config)
    if total_column==good_column or any(c not in rows[0] for c in (total_column,good_column)):raise ValidationError('Distinct existing total/good columns required')
    values=[]
    for row in rows:
        total,good=finite_number(row[total_column]),finite_number(row[good_column])
        if total is None or good is None or total<0 or not 0<=good<=total:raise ValidationError('Counts must be finite and 0<=good<=total')
        values.append((total,good))
    total=sum(v[0] for v in values);good=sum(v[1] for v in values)
    if total<=0:raise ValidationError('Total production must be positive')
    result={'total_units':total,'good_units':good,'rejected_units':total-good,'yield_fraction':good/total,'reject_fraction':(total-good)/total}
    if operating_hours is not None:
        if finite_number(operating_hours)is None or operating_hours<=0:raise ValidationError('Explicit positive finite operating_hours required')
        result['units_per_operating_hour']=total/operating_hours
    return Result('industry.production',result,'stdlib.production-accounting',['No OEE is claimed without planned time, availability, ideal cycle time and consistent definitions. Check units, duplicate shifts and count provenance.'])


def maintenance(*,data,target,config):
    from .ml import train
    trained=train(data=data,target=target,problem='classification',config=config)
    result=trained.report;result.task='industry.maintenance'
    result.warnings.extend(['Supervised historical-label classifier, not calibrated failure probability or remaining useful life. Random split is a teaching baseline; asset/time grouped validation is required before production maintenance decisions. No automatic shutdown or actuation.'])
    return result


def defects(*,image,reference,config,threshold=25,min_area=20,output=None):
    from .core import input_file
    cv2=require('cv2','vision');a=input_file(image,config);b=input_file(reference,config)
    if type(threshold)is not int or not 1<=threshold<=254 or not 1<=float(min_area)<=1e9:raise ValidationError('threshold 1..254 and positive min_area required')
    inspected=cv2.imread(str(a));standard=cv2.imread(str(b))
    if inspected is None or standard is None or inspected.shape!=standard.shape:raise ValidationError('Decodable, aligned, same-size image and known-good reference required')
    if inspected.shape[0]*inspected.shape[1]>20_000_000:raise ValidationError('Images exceed 20MP limit')
    aa=cv2.cvtColor(inspected,cv2.COLOR_BGR2GRAY);bb=cv2.cvtColor(standard,cv2.COLOR_BGR2GRAY)
    difference=cv2.absdiff(aa,bb);mask=cv2.threshold(difference,threshold,255,cv2.THRESH_BINARY)[1]
    contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    boxes=[dict(zip(('x','y','width','height'),map(int,cv2.boundingRect(c)))) for c in contours if cv2.contourArea(c)>=min_area]
    if output is not None:
        path=Path(output)
        if path.suffix.lower()!='.png':raise ValidationError('Difference mask output must be PNG')
        path.parent.mkdir(parents=True,exist_ok=True);ok,encoded=cv2.imencode('.png',mask)
        if not ok:raise ValidationError('Mask encoding failed')
        with path.open('xb') as stream:stream.write(encoded.tobytes())
    return Result('industry.defects',{'candidate_count':len(boxes),'changed_fraction':cv2.countNonZero(mask)/mask.size,'rows':boxes,'mask_path':str(output) if output else None},'opencv.aligned-reference-difference',['Difference candidates, NOT a semantic defect diagnosis or validated factory acceptance rule. Lighting, pose and alignment changes can cause false alarms. Requires a representative known-good reference.'],{'image_sha256':fingerprint(a),'reference_sha256':fingerprint(b)})
