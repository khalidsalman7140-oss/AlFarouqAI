# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Public contracts, bounded inputs, explicit configuration and portable exports."""
from __future__ import annotations
import csv
import hashlib
import html
import importlib
import importlib.metadata
import json
import math
import os
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

__version__ = '0.3.0a1'

class AlFarouqError(Exception):
    """Actionable base exception; never converted to a fake success."""

class ValidationError(AlFarouqError):
    pass

class MissingDependency(AlFarouqError):
    pass

class ConsentRequired(AlFarouqError):
    pass

class UnsupportedTask(AlFarouqError):
    pass


def require(module: str, extra: str):
    if module in ('transformers', 'sentence_transformers'):
        # These adapters are PyTorch-specific; avoid accidental Keras backend imports.
        os.environ.setdefault('USE_TF', '0')
    try:
        return importlib.import_module(module)
    except ImportError as exc:
        raise MissingDependency(f"Install the optional '{extra}' extra in your chosen environment: from this checkout use: pip install '.[{extra}]'. Nothing was installed automatically.") from exc


@dataclass(frozen=True)
class Config:
    """Local-only defaults. Model locations must be supplied explicitly."""
    max_input_bytes: int = 20_000_000
    max_rows: int = 100_000
    max_video_frames: int = 300
    max_agent_steps: int = 12
    timeout: float = 60.0
    ollama_url: str = 'http://127.0.0.1:11434'
    model: str | None = None
    allow_network: bool = False
    allow_remote: bool = False
    allow_model_download: bool = False
    verbose: bool = False

    def __post_init__(self):
        for name in ('max_input_bytes', 'max_rows', 'max_video_frames', 'max_agent_steps'):
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise ValidationError(f'{name} must be a positive integer')
        if not isinstance(self.timeout, (int, float)) or not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValidationError('timeout must be finite and positive')
        for name in ('allow_network', 'allow_remote', 'allow_model_download', 'verbose'):
            if type(getattr(self, name)) is not bool:
                raise ValidationError(f'{name} must be a boolean, not a string')
        if not isinstance(self.ollama_url, str) or (self.model is not None and not isinstance(self.model, str)):
            raise ValidationError('ollama_url and model must be strings (model may be None)')

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValidationError('Config must be a JSON object')
        unknown = set(data) - set(cls.__dataclass_fields__)
        if unknown:
            raise ValidationError(f'Unknown config keys: {sorted(unknown)}')
        return cls(**data)

    def save(self, path):
        return atomic_write(path, json.dumps(asdict(self), indent=2), overwrite=False)


def atomic_write(path, text: str, *, overwrite=False):
    """Exclusive creation by default; existing user files are never silently replaced."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not overwrite:
        with path.open('x', encoding='utf-8', newline='') as stream:
            stream.write(text)
        return path
    fd, name = tempfile.mkstemp(prefix='.alfarouq-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as stream:
            stream.write(text)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return path


def input_file(path, config: Config):
    p = Path(path).expanduser()
    if not p.is_file():
        raise ValidationError(f'Input file not found: {p}')
    if p.stat().st_size > config.max_input_bytes:
        raise ValidationError(f'Input exceeds {config.max_input_bytes} bytes')
    return p


def fingerprint(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            digest.update(block)
    return digest.hexdigest()


def clean_json(value):
    if isinstance(value, dict):
        return {str(k): clean_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean_json(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if hasattr(value, 'tolist'):
        return clean_json(value.tolist())
    if hasattr(value, 'item'):
        return clean_json(value.item())
    if isinstance(value, Path):
        return str(value)
    return value


@dataclass
class Result:
    task: str
    data: dict
    backend: str
    warnings: list[str] = field(default_factory=list)
    provenance: dict = field(default_factory=dict)
    schema_version: str = '1.0'

    def to_dict(self):
        return clean_json(asdict(self))

    def export(self, path, *, overwrite=False):
        """JSON/Markdown/HTML/TXT reports; CSV contains data.rows or scalar fields."""
        import io
        path = Path(path)
        ext = path.suffix.lower()
        obj = self.to_dict()
        raw = json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)
        if ext == '.json':
            text = raw
        elif ext in ('.md', '.txt'):
            text = f'# AlFarouq AI — {self.task}\n\nBackend: {self.backend}\n\n```json\n{raw}\n```\n'
        elif ext == '.html':
            text = '<!doctype html><html lang="en"><meta charset="utf-8"><title>AlFarouq AI report</title><style>body{max-width:1050px;margin:3em auto;font:16px system-ui;padding:1em}pre{white-space:pre-wrap;background:#f1f5f9;padding:1em}</style><h1>AlFarouq AI</h1><pre>' + html.escape(raw) + '</pre></html>'
        elif ext == '.csv':
            rows = self.data.get('rows')
            if rows is None:
                rows = [{'key': k, 'value': v if isinstance(v, (str, int, float, bool)) else json.dumps(clean_json(v), ensure_ascii=False)} for k, v in self.data.items()]
            if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
                raise ValidationError('CSV export needs a list of dictionaries in data.rows')
            keys = list(dict.fromkeys(k for row in rows for k in row))
            stream = io.StringIO(newline='')
            writer = csv.DictWriter(stream, fieldnames=keys)
            writer.writeheader()
            for row in rows:
                safe = {}
                for k, v in row.items():
                    if isinstance(v, (dict, list, tuple)):
                        v = json.dumps(clean_json(v), ensure_ascii=False)
                    # Spreadsheet formula injection protection, including prefixed whitespace.
                    if isinstance(v, str) and v.lstrip().startswith(('=', '+', '-', '@')):
                        v = "'" + v
                    safe[k] = v
                writer.writerow(safe)
            text = stream.getvalue()
        else:
            raise ValidationError('Supported exports: .json .csv .md .html .txt')
        return atomic_write(path, text, overwrite=overwrite)


@dataclass(frozen=True)
class Capability:
    name: str
    handler: Callable
    description: str
    required: tuple[str, ...] = ()
    extra: str | None = None
    status: str = 'implemented'


class Registry:
    def __init__(self):
        self._items: dict[str, Capability] = {}

    def register(self, capability: Capability):
        if capability.name in self._items:
            raise ValidationError(f'Duplicate capability: {capability.name}')
        self._items[capability.name] = capability

    def get(self, name):
        if name not in self._items:
            raise UnsupportedTask(f'Unknown capability {name!r}; inspect Client.capabilities()')
        return self._items[name]

    def list(self):
        return [{'name': c.name, 'description': c.description, 'required': list(c.required), 'extra': c.extra, 'status': c.status} for c in self._items.values()]

    def load_plugins(self, *, consent=False):
        if not consent:
            raise ConsentRequired('Plugins execute installed Python code. Pass consent=True only for trusted plugins.')
        eps = importlib.metadata.entry_points(group='alfarouqai.plugins')
        names = []
        for ep in eps:
            ep.load()(self)
            names.append(ep.name)
        return names


def timed_result(capability, inputs, config):
    import inspect
    started = time.perf_counter()
    signature = inspect.signature(capability.handler)
    permitted = {name for name, param in signature.parameters.items() if name != 'config' and param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD)}
    unknown = set(inputs) - permitted
    if unknown:
        raise ValidationError(f'Unknown inputs for {capability.name}: {sorted(unknown)}')
    for name in capability.required:
        if name not in inputs or inputs[name] is None:
            raise ValidationError(f'{capability.name} requires {name!r}')
    result = capability.handler(config=config, **inputs)
    if not isinstance(result, Result):
        raise ValidationError('Capability must return a Result')
    result.provenance.update({'library_version': __version__, 'elapsed_seconds': round(time.perf_counter() - started, 6), 'network_policy': 'explicit opt-in', 'executed': True})
    return result
