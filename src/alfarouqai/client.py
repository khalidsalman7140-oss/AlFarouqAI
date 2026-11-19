# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Unified high-level API with explainable, conservative bilingual routing."""
from __future__ import annotations
from .core import Capability, Config, Registry, Result, ValidationError, UnsupportedTask, timed_result
from . import local, media, documents, providers, ml


def default_registry():
    registry = Registry()
    definitions = [
        ('text.analyze', local.text_analyze, 'Extractive Arabic/English text statistics and summary', ('text',), None),
        ('data.profile', local.data_profile, 'Profile a UTF-8 CSV with missing values and numeric statistics', ('data',), None),
        ('ml.train', ml.train_report, 'Train/test a RandomForest with explicit target/problem', ('data', 'target', 'problem'), 'ml'),
        ('image.analyze', media.image_analyze, 'Local image statistics and frontal face detection', ('image',), 'vision'),
        ('image.objects', media.objects_detect, 'General object detection using reviewed local model weights', ('image', 'model_path'), 'objects'),
        ('video.motion', media.video_motion, 'Bounded frame-difference motion regions', ('video',), 'vision'),
        ('audio.info', media.audio_info, 'PCM WAV metadata', ('audio',), None),
        ('speech.transcribe', media.transcribe, 'Whisper transcription with an explicit local model', ('audio',), 'speech'),
        ('document.read', documents.document_read, 'Extract text from TXT/PDF/DOCX/XLSX', ('document',), 'documents'),
        ('code.analyze', local.code_analyze, 'Non-executing Python AST and project review', (), None),
        ('security.logs', local.security_logs, 'Defensive authentication log analysis', ('path',), None),
        ('iot.analyze', local.sensor_analyze, 'Offline sensor time-series z-score anomaly flags', ('data', 'column'), None),
        ('llm.chat', providers.chat, 'Opt-in Ollama text and supported vision chat', ('prompt',), None),
    ]
    for name, handler, desc, required, extra in definitions:
        registry.register(Capability(name, handler, desc, required, extra))
    from .extensions import register_extensions
    register_extensions(registry)
    from .services import register_services
    register_services(registry)
    return registry


class Client:
    def __init__(self, config=None, registry=None):
        self.config = config or Config()
        self.registry = registry or default_registry()

    def capabilities(self):
        return self.registry.list()

    SHORTCUTS = {'ar':'arabic.process', 'sales':'sales.forecast', 'qc':'industry.defects', 'sensors':'industry.sensors', 'db':'database.profile', 'redact':'privacy.redact', 'astar':'ai.search'}

    def run(self, task, *, verbose=None, **inputs):
        import sys
        task = self.SHORTCUTS.get(task, task)
        enabled = self.config.verbose if verbose is None else bool(verbose)
        if enabled: print(f'[AlFarouq AI] start task={task}', file=sys.stderr)
        try:
            result = timed_result(self.registry.get(task), inputs, self.config)
        except Exception as exc:
            if enabled: print(f'[AlFarouq AI] error task={task} type={type(exc).__name__}', file=sys.stderr)
            raise
        if enabled: print(f'[AlFarouq AI] done task={task} backend={result.backend} seconds={result.provenance.get("elapsed_seconds")}', file=sys.stderr)
        return result

    def ar(self, text, **kwargs): return self.run('arabic.process', text=text, **kwargs)
    def sales(self, data, **kwargs): return self.run('sales.forecast', data=data, **kwargs)
    def inspect(self, image, reference, **kwargs): return self.run('industry.defects', image=image, reference=reference, **kwargs)
    def file(self, document, **kwargs): return self.run('document.insights', document=document, **kwargs)
    def text_train(self, **kwargs):
        from .arabic import train_text
        return train_text(config=self.config, **kwargs)


    def train(self, *, data, target, problem, **kwargs):
        return ml.train(data=data, target=target, problem=problem, config=self.config, **kwargs)

    def deep_train(self, **kwargs):
        from .learning import train_neural
        return train_neural(config=self.config, **kwargs)

    def prepare(self, task, environment, *, consent=False):
        from .dependencies import installation_plan, install_extra
        cap = self.registry.get(task)
        if not cap.extra:
            return {'task': task, 'extra': None, 'note': 'No Python extra required; system executables may still be needed.'}
        return install_extra(cap.extra, environment, consent=True) if consent else installation_plan(cap.extra, environment)

    def plan(self, prompt, **inputs):
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValidationError('A nonempty prompt is required')
        prompt = self.SHORTCUTS.get(prompt, prompt)
        if 'file' in inputs:
            inputs = dict(inputs)
            if 'document' in inputs: raise ValidationError('Use either file or document, not both')
            inputs['document'] = inputs.pop('file')
        if prompt in {c['name'] for c in self.capabilities()}:
            cap = self.registry.get(prompt)
            return {'task': prompt, 'required': list(cap.required), 'missing': [k for k in cap.required if k not in inputs], 'extra': cap.extra, 'planner': 'explicit task shorthand', 'executes': False}
        p = prompt.casefold()
        groups = [key for key in ('image', 'video', 'audio', 'data', 'document', 'code', 'path', 'text') if inputs.get(key) is not None]
        if len(groups) > 1:
            raise UnsupportedTask('Ambiguous multiple inputs. Use Client.run(task, ...) or compose explicit AgentTeam steps.')
        service = None
        if 'image' in groups and any(t in p for t in ('عيوب', 'عيب', 'defect', 'quality')): service = 'industry.defects'
        elif 'data' in groups and any(t in p for t in ('مبيعات', 'المبيعات', 'sales')): service = 'sales.forecast'
        elif 'text' in groups and any(t in p for t in ('العربية', 'عربي', 'arabic')): service = 'arabic.process'
        elif 'document' in groups and any(t in p for t in ('استخرج', 'أهم المعلومات', 'extract', 'insights')): service = 'document.insights'
        if service:
            cap = self.registry.get(service)
            return {'task':service, 'required':list(cap.required), 'missing':[k for k in cap.required if k not in inputs], 'extra':cap.extra, 'planner':'explicit service phrase router', 'executes':False}
        if 'image' in groups:
            if any(k in p for k in ('object', 'أشياء', 'الأشياء', 'كائنات', 'اجسام', 'أجسام')):
                task = 'image.objects'
            elif any(k in p for k in ('analy', 'face', 'حلل', 'تحليل', 'وجه', 'وجوه', 'صورة')):
                task = 'image.analyze'
            else:
                raise UnsupportedTask('Image request not understood; choose image.analyze, image.objects or llm.chat explicitly')
        elif 'video' in groups:
            if any(k in p for k in ('person', 'people', 'أشخاص', 'الأشخاص', 'تتبع', 'tracking', 'action')):
                raise UnsupportedTask('Person/action tracking is not implemented. video.motion only detects motion regions.')
            task = 'video.motion'
        elif 'audio' in groups:
            task = 'speech.transcribe' if any(k in p for k in ('transcri', 'speech to text', 'فرغ', 'تفريغ', 'إلى نص', 'الى نص')) else 'audio.info'
        elif 'document' in groups:
            if any(k in p for k in ('summar', 'لخص', 'تلخيص', 'answer', 'أجب')):
                raise UnsupportedTask('Compose document.read -> text.analyze in AgentTeam for an extractive summary, or use an explicit LLM workflow.')
            task = 'document.read'
        elif 'data' in groups:
            if any(k in p for k in ('predict', 'train', 'model', 'تنبؤ', 'التنبؤ', 'نموذج', 'تدريب')):
                task = 'ml.train'
            elif any(k in p for k in ('sensor', 'anomal', 'مستشعر', 'حساس', 'شذوذ')):
                task = 'iot.analyze'
            elif any(k in p for k in ('analy', 'profile', 'statistics', 'حلل', 'تحليل', 'إحصاء')):
                task = 'data.profile'
            else:
                raise UnsupportedTask('CSV request not understood; specify data.profile, ml.train or iot.analyze')
        elif 'code' in groups or ('path' in groups and any(k in p for k in ('code', 'project', 'كود', 'مشروع'))):
            task = 'code.analyze'
        elif 'path' in groups and any(k in p for k in ('log', 'security', 'سجل', 'أمن')):
            task = 'security.logs'
        elif 'text' in groups:
            if not any(k in p for k in ('analy', 'summar', 'keyword', 'حلل', 'تحليل', 'لخص', 'تلخيص')):
                raise UnsupportedTask('Use text.analyze for extractive analysis or llm.chat explicitly for generation')
            task = 'text.analyze'
        elif self.config.model:
            task = 'llm.chat'
        else:
            task = 'local.generate'  # Generic prompt is text generation, not arbitrary tool execution.
        cap = self.registry.get(task)
        return {'task': task, 'required': list(cap.required), 'missing': [k for k in cap.required if k not in inputs and k != 'prompt'], 'extra': cap.extra, 'planner': 'bilingual deterministic router', 'executes': False}

    def __call__(self, prompt, **inputs):
        if 'file' in inputs:
            if 'document' in inputs: raise ValidationError('Use either file or document, not both')
            inputs['document'] = inputs.pop('file')
        explicit = inputs.pop('task', None)
        if explicit is not None:
            if explicit in ('local.generate', 'code.generate', 'image.generate', 'video.generate', 'llm.chat'):
                inputs.setdefault('prompt', prompt)
            return self.run(explicit, **inputs)
        plan = self.plan(prompt, **inputs)
        if plan['missing']:
            raise ValidationError(f"{plan['task']} needs explicit fields: {', '.join(plan['missing'])}. Nothing was inferred or executed.")
        if plan['task'] in ('llm.chat', 'local.generate'):
            inputs['prompt'] = prompt
        return self.run(plan['task'], **inputs)


def AI(prompt, *, config=None, model=None, backend='auto', endpoint=None, api_key_env=None, device='auto', **inputs):
    """One-call services or explicit model gateway; no hidden installs or hardware promises."""
    if model is not None:
        from .shortcut import model_call
        unknown = set(inputs) - {'max_new_tokens'}
        if unknown: raise ValidationError(f'Model gateway does not accept service inputs: {sorted(unknown)}')
        return model_call(prompt, model=model, backend=backend, endpoint=endpoint, config=config, api_key_env=api_key_env, device=device, **inputs)
    if backend != 'auto' or endpoint is not None or api_key_env is not None:
        raise ValidationError('Specify model= when selecting a model backend or endpoint')
    return Client(config)(prompt, **inputs)
