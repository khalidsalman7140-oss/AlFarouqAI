# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Optional local ONNX/Keras inference and explicitly approved HTTP inference."""
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request
import urllib.error
from .core import Result,ValidationError,ConsentRequired,AlFarouqError,require,input_file


def onnx_predict(*,model_path,inputs,config):
    np=require('numpy','onnx');onnx=require('onnx','onnx');ort=require('onnxruntime','onnx')
    p=input_file(model_path,config)
    model=onnx.load_model(str(p),load_external_data=False)
    if any(t.data_location==onnx.TensorProto.EXTERNAL for t in model.graph.initializer):raise ValidationError('External ONNX tensor data is not accepted')
    onnx.checker.check_model(model)
    session=ort.InferenceSession(model.SerializeToString(),providers=['CPUExecutionProvider'])
    if not isinstance(inputs,dict) or set(inputs)!={i.name for i in session.get_inputs()}:raise ValidationError('Input keys must exactly match ONNX model inputs')
    types={'tensor(float)':'float32','tensor(double)':'float64','tensor(int64)':'int64','tensor(int32)':'int32','tensor(bool)':'bool'};feed={};size=0
    for spec in session.get_inputs():
        if spec.type not in types:raise ValidationError('Unsupported ONNX tensor type')
        a=np.asarray(inputs[spec.name],dtype=types[spec.type]);size+=a.nbytes
        if size>config.max_input_bytes:raise ValidationError('ONNX input byte budget exceeded')
        if a.ndim!=len(spec.shape) or any(isinstance(n,int) and n!=v for n,v in zip(spec.shape,a.shape)):raise ValidationError('ONNX tensor shape mismatch')
        if a.dtype.kind=='f' and not np.isfinite(a).all():raise ValidationError('Finite inputs required')
        feed[spec.name]=a
    outputs=session.run(None,feed)
    return Result('onnx.predict',{'outputs':{meta.name:value.tolist() for meta,value in zip(session.get_outputs(),outputs)}},'onnxruntime.CPUExecutionProvider',['Only reviewed local models; native runtime is not an OS sandbox. External tensor data and custom-op libraries are not loaded by this adapter.'])


def tensorflow_predict(*,model_path,inputs,config):
    if not isinstance(inputs,list):raise ValidationError('Keras adapter expects a JSON-style numeric input array')
    p=input_file(model_path,config)
    if p.suffix!='.keras':raise ValidationError('Only reviewed local .keras files are supported')
    tf=require('tensorflow','tensorflow');np=require('numpy','tensorflow')
    try:
        tf.config.threading.set_intra_op_parallelism_threads(1);tf.config.threading.set_inter_op_parallelism_threads(1)
    except RuntimeError:
        pass  # Respect a TensorFlow runtime that the caller already initialized.
    a=np.asarray(inputs,dtype='float32')
    if a.nbytes>config.max_input_bytes or a.size==0 or not np.isfinite(a).all():raise ValidationError('Bounded nonempty finite input array required')
    model=tf.keras.models.load_model(str(p),safe_mode=True,compile=False)
    result=model(a,training=False)
    if not hasattr(result,'numpy'):raise ValidationError('Only single-tensor Keras outputs supported')
    return Result('tensorflow.predict',{'outputs':result.numpy().tolist()},'tensorflow.keras.cpu',['safe_mode is defense in depth, not permission to load hostile files. Reviewed models only; no custom objects or training API claimed.'])


def compatible_chat(*,prompt,endpoint,model,config,api_key_env=None,max_tokens=80):
    from .providers import NoRedirect
    if not config.allow_network:raise ConsentRequired('HTTP inference requires allow_network=True')
    url=urllib.parse.urlsplit(endpoint)
    if url.scheme not in ('http','https') or not url.hostname or url.username or url.password or url.query or url.fragment:raise ValidationError('Clean http(s) endpoint without credentials/query required')
    if url.hostname not in ('127.0.0.1','localhost','::1'):
        if not config.allow_remote:raise ConsentRequired('Remote inference needs allow_remote=True')
        if url.scheme!='https':raise ValidationError('Remote inference requires HTTPS')
    if not isinstance(prompt,str) or not prompt.strip() or len(prompt.encode())>config.max_input_bytes or not isinstance(model,str) or not model or type(max_tokens)is not int or not 1<=max_tokens<=1024:raise ValidationError('Bounded prompt/model and max_tokens required')
    headers={'Content-Type':'application/json'}
    if api_key_env:
        if not isinstance(api_key_env,str) or not api_key_env.replace('_','').isalnum():raise ValidationError('Use an environment-variable name, never a literal API key')
        key=os.environ.get(api_key_env)
        if not key:raise ValidationError('Selected API key environment variable is empty')
        headers['Authorization']='Bearer '+key
    raw=json.dumps({'model':model,'messages':[{'role':'user','content':prompt}],'max_tokens':max_tokens,'stream':False,'temperature':0}).encode()
    request=urllib.request.Request(endpoint.rstrip('/')+'/chat/completions',data=raw,headers=headers)
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    try:
        with opener.open(request,timeout=config.timeout) as response:content=response.read(config.max_input_bytes+1)
    except (urllib.error.URLError,OSError) as exc:raise AlFarouqError('Compatible inference request failed; endpoint/model/status should be checked without logging secrets') from exc
    if len(content)>config.max_input_bytes:raise ValidationError('HTTP response byte budget exceeded')
    try:obj=json.loads(content);text=obj['choices'][0]['message']['content']
    except (ValueError,KeyError,IndexError,TypeError) as exc:raise ValidationError('Invalid OpenAI-compatible response envelope') from exc
    if not isinstance(text,str):raise ValidationError('Expected textual model response')
    return Result('llm.compatible',{'text':text,'model':obj.get('model',model)},'openai-compatible-http',['Protocol compatible with vLLM-like endpoints; no claim that a particular third-party server or cloud model was deployed/tested. Provider terms/costs remain user responsibility.'])
