# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Reviewed official TorchVision weights, OCR and temporary object track IDs."""
from pathlib import Path
import csv
import io
import math
import re
import shutil
import subprocess
from .core import Result, ValidationError, MissingDependency, input_file, require, fingerprint
from .models import prepare

class VisionEngine:
    def __init__(self,kind,config):
        self.config=config; self.kind=kind
        torch=require('torch','torchvision');tv=require('torchvision','torchvision')
        torch.set_num_threads(2);self.torch=torch
        paths={'detect':'ssdlite320','classify':'mobilenet-v3','segment':'lraspp'}
        root=prepare(paths[kind],config=config)
        if kind=='detect':
            self.weights=tv.models.detection.SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
            self.model=tv.models.detection.ssdlite320_mobilenet_v3_large(weights=None,weights_backbone=None)
        elif kind=='segment':
            self.weights=tv.models.segmentation.LRASPP_MobileNet_V3_Large_Weights.DEFAULT
            self.model=tv.models.segmentation.lraspp_mobilenet_v3_large(weights=None,weights_backbone=None)
        else:
            self.weights=tv.models.MobileNet_V3_Small_Weights.DEFAULT
            self.model=tv.models.mobilenet_v3_small(weights=None)
        self.model.load_state_dict(torch.load(root/'weights.pth',map_location='cpu',weights_only=True))
        self.model.eval();self.transforms=self.weights.transforms();self.categories=self.weights.meta['categories']

    def image(self,image):
        PIL=require('PIL.Image','torchvision');p=input_file(image,self.config)
        with PIL.open(p) as source:
            if source.width*source.height>20_000_000:raise ValidationError('Image exceeds 20 megapixels')
            return source.convert('RGB')

    def detect(self,im,threshold=.4):
        with self.torch.inference_mode():pred=self.model([self.transforms(im)])[0]
        return [{'label':self.categories[int(l)],'label_id':int(l),'score':float(s),'box_xyxy':[round(float(x),2) for x in b]} for l,s,b in zip(pred['labels'],pred['scores'],pred['boxes']) if float(s)>=threshold]


def detect(*,image,config,threshold=.4):
    if not 0<threshold<=1:raise ValidationError('threshold must be in (0,1]')
    engine=VisionEngine('detect',config)
    rows=engine.detect(engine.image(image),threshold)
    return Result('vision.detect',{'rows':rows},'torchvision.ssdlite320-coco',['Object detections are uncertain, not identity recognition. COCO category coverage is limited.'],{'input_sha256':fingerprint(image),'actual_weight_inference':True,'weights':'SSDLite320_MobileNet_V3_Large_Weights.COCO_V1'})


def classify(*,image,config,top_k=5):
    if type(top_k)is not int or not 1<=top_k<=1000:raise ValidationError('top_k must be 1..1000')
    engine=VisionEngine('classify',config);im=engine.image(image)
    with engine.torch.inference_mode():probs=engine.model(engine.transforms(im).unsqueeze(0)).softmax(dim=1)[0]
    scores,labels=probs.topk(top_k)
    rows=[{'label':engine.categories[int(i)],'score':float(s)} for i,s in zip(labels,scores)]
    return Result('vision.classify',{'rows':rows},'torchvision.mobilenet-v3-small',['ImageNet labels are not a universal image understanding vocabulary.'],{'actual_weight_inference':True,'input_sha256':fingerprint(image)})


def segment(*,image,config,output):
    engine=VisionEngine('segment',config);im=engine.image(image)
    torch=engine.torch
    with torch.inference_mode():
        logits=engine.model(engine.transforms(im).unsqueeze(0))['out']
        resized=torch.nn.functional.interpolate(logits,size=(im.height,im.width),mode='bilinear',align_corners=False)
        mask=resized.argmax(1)[0].to(torch.uint8).cpu().numpy()
    PIL=require('PIL.Image','torchvision');path=Path(output)
    if path.suffix.lower()!='.png':raise ValidationError('Segmentation output must be a new PNG file')
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:PIL.fromarray(mask).save(f,format='PNG')
    import numpy as np
    ids,counts=np.unique(mask,return_counts=True)
    rows=[{'class_id':int(i),'label':engine.categories[int(i)],'pixels':int(n)} for i,n in zip(ids,counts)]
    return Result('vision.segment',{'mask_path':str(path),'width':im.width,'height':im.height,'rows':rows},'torchvision.lraspp-voc',['Semantic class mask (pixel values are class IDs), not individual-instance segmentation.'],{'actual_weight_inference':True,'input_sha256':fingerprint(image)})


def ocr(*,image,config,language='eng',psm=6):
    p=input_file(image,config)
    exe=shutil.which('tesseract')
    if not exe:raise MissingDependency('Install the optional system Tesseract OCR executable and desired language packs yourself; no automatic OS installation')
    if not re.fullmatch(r'[A-Za-z0-9_]+(?:\+[A-Za-z0-9_]+)*',language) or type(psm)is not int or not 0<=psm<=13:
        raise ValidationError('Invalid OCR language/PSM')
    proc=subprocess.run([exe,str(p.resolve()),'stdout','-l',language,'--psm',str(psm),'tsv'],capture_output=True,text=True,timeout=config.timeout,shell=False)
    if proc.returncode:raise ValidationError('Tesseract failed: '+proc.stderr[-1500:])
    rows=[];lines={}
    for r in csv.DictReader(io.StringIO(proc.stdout),delimiter='\t'):
        if not r.get('text','').strip():continue
        row={'text':r['text'],'confidence':float(r['conf']),'x':int(r['left']),'y':int(r['top']),'width':int(r['width']),'height':int(r['height'])}
        rows.append(row);key=(r['page_num'],r['block_num'],r['par_num'],r['line_num']);lines.setdefault(key,[]).append(r['text'])
    return Result('vision.ocr',{'text':'\n'.join(' '.join(words) for words in lines.values()),'rows':rows,'language':language},'tesseract.system',['Recognition depends on scan quality and installed language packs; Arabic quality not guaranteed.'],{'actual_model_inference':True,'input_sha256':fingerprint(p)})


class CentroidTracker:
    """Temporary IDs only; greedy same-label association, no biometric recognition."""
    def __init__(self,max_distance=100,max_missed=5):self.tracks={};self.next_id=1;self.max_distance=max_distance;self.max_missed=max_missed
    def update(self,detections):
        unmatched=set(self.tracks);rows=[]
        for d in sorted(detections,key=lambda r:-r.get('score',1)):
            x1,y1,x2,y2=d['box_xyxy'];center=((x1+x2)/2,(y1+y2)/2)
            candidates=[(math.dist(center,self.tracks[i]['center']),i) for i in unmatched if self.tracks[i]['label']==d['label']]
            distance,idx=min(candidates,default=(float('inf'),None))
            if distance>self.max_distance:idx=self.next_id;self.next_id+=1
            else:unmatched.remove(idx)
            self.tracks[idx]={'center':center,'label':d['label'],'missed':0}
            rows.append({**d,'track_id':idx})
        for i in unmatched:
            self.tracks[i]['missed']+=1
            if self.tracks[i]['missed']>self.max_missed:del self.tracks[i]
        return rows


def track(*,video,config,max_frames=30,threshold=.4):
    if type(max_frames)is not int or not 1<=max_frames<=config.max_video_frames or not 0<threshold<=1:raise ValidationError('Invalid frame budget/threshold')
    cv2=require('cv2','vision');PIL=require('PIL.Image','torchvision');p=input_file(video,config)
    engine=VisionEngine('detect',config);tracker=CentroidTracker();cap=cv2.VideoCapture(str(p));rows=[]
    if not cap.isOpened():raise ValidationError('Cannot open video')
    fps=cap.get(cv2.CAP_PROP_FPS)
    try:
        for i in range(max_frames):
            ok,frame=cap.read()
            if not ok:break
            if frame.shape[0]*frame.shape[1]>20_000_000:raise ValidationError('Frame too large')
            im=PIL.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            rows.append({'frame':i,'time_seconds':i/fps if fps>0 else None,'objects':tracker.update(engine.detect(im,threshold))})
        more=cap.read()[0] if len(rows)==max_frames else False
    finally:cap.release()
    if not rows:raise ValidationError('No video frames decoded')
    return Result('video.track',{'rows':rows,'truncated':bool(more),'processed_frames':len(rows)},'torchvision.ssdlite+centroid-tracker',['Temporary same-class centroid tracks; can swap IDs under occlusion/crossing. Not action recognition or identity.'],{'actual_weight_inference':True,'input_sha256':fingerprint(p)})
