# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Inspect dependencies without importing heavy engines; install only in owned venvs."""
from __future__ import annotations
import importlib.metadata
import json
import subprocess
import sys
import venv
from pathlib import Path
from .core import ConsentRequired, ValidationError

EXTRAS = {
    'ml': ['scikit-learn>=1.5,<2', 'pandas>=2.2,<4'],
    'vision': ['opencv-python-headless>=4.10,<5'],
    'documents': ['pypdf>=5,<7', 'python-docx>=1.1,<2', 'openpyxl>=3.1,<4'],
    'speech': ['faster-whisper>=1.1,<2', 'av>=11,<16'],
    'semantic': ['sentence-transformers>=3,<6'],
    'objects': ['transformers>=4.45,<6', 'torch>=2.5,<3', 'Pillow>=10.4,<14', 'safetensors>=0.4,<1'],
    'persistence': ['skops>=0.11,<1'],
    'local': ['transformers>=4.46,<5', 'torch>=2.6,<3', 'safetensors>=0.4,<1'],
    'torchvision': ['torch>=2.6,<3', 'torchvision>=0.21,<1', 'Pillow>=10.4,<14'],
    'deep': ['torch>=2.6,<3', 'safetensors>=0.4,<1', 'scikit-learn>=1.5,<2', 'pandas>=2.2,<4'],
    'vector': ['sentence-transformers>=3.3,<6', 'faiss-cpu>=1.8,<2'],
    'iot': ['pyserial>=3.5,<4', 'paho-mqtt>=2,<3'],
    'diffusion': ['diffusers>=0.31,<1', 'transformers>=4.46,<5', 'torch>=2.6,<3', 'accelerate>=1,<2', 'safetensors>=0.4,<1', 'imageio-ffmpeg>=0.5,<1'],
    'nlp': ['nltk>=3.9,<4', 'scikit-learn>=1.5,<2'],
    'api': ['fastapi>=0.115,<1', 'uvicorn>=0.30,<1', 'httpx>=0.27,<1'],
    'onnx': ['onnx>=1.17,<2', 'onnxruntime>=1.20,<2'],
    'tensorflow': ['tensorflow-cpu>=2.20,<3'],
    'industrial': ['pymodbus>=3.11,<4'],
    'gdrive': ['google-api-python-client>=2,<3', 'google-auth-oauthlib>=1,<2'],
    'dev': ['pytest>=8,<10', 'build>=1.2,<2', 'twine>=6,<7'],
}


def doctor():
    items = {}
    for extra, specs in EXTRAS.items():
        items[extra] = {}
        for spec in specs:
            name = spec.split('>=')[0]
            try:
                version = importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError:
                version = None
            items[extra][name] = {'installed_version': version, 'declared_constraint': spec, 'note': 'Presence only; this does not assert version compatibility'}
    return {'python': sys.version.split()[0], 'executable': sys.executable, 'extras': items, 'network_on_import': False}


def installation_plan(extra, environment):
    if extra not in EXTRAS:
        raise ValidationError(f'Unknown extra. Choose {sorted(EXTRAS)}')
    root = Path(environment).expanduser().absolute()
    exe = root / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    return {'extra': extra, 'environment': str(root), 'packages': EXTRAS[extra], 'command': [str(exe), '-m', 'pip', '--isolated', 'install', '--index-url', 'https://pypi.org/simple', *EXTRAS[extra]], 'notice': 'May download dependencies and execute package build code. Review licenses and the PyPI supply chain. No model weights are included.'}


def install_extra(extra, environment, *, consent=False, timeout=600):
    plan = installation_plan(extra, environment)
    if not consent:
        raise ConsentRequired(json.dumps(plan, indent=2) + '\nPass consent=True only after review.')
    root = Path(plan['environment'])
    marker = root / '.alfarouq-managed.json'
    # Never alter an unrelated/existing user environment or the running interpreter.
    if root.is_symlink() or root.resolve() == Path(sys.prefix).resolve():
        raise ValidationError('Unsafe environment location')
    if root.exists() and not marker.is_file():
        raise ValidationError('Existing directory is not an AlFarouq-managed virtual environment')
    if not root.exists():
        venv.EnvBuilder(with_pip=True).create(root)
        marker.write_text(json.dumps({'managed_by': 'alfarouqai', 'purpose': 'optional dependencies'}), encoding='utf-8')
    else:
        try:
            if json.loads(marker.read_text())['managed_by'] != 'alfarouqai':
                raise ValueError('marker')
        except (ValueError, KeyError) as exc:
            raise ValidationError('Invalid managed-environment marker') from exc
    completed = subprocess.run(plan['command'], shell=False, capture_output=True, text=True, timeout=timeout, check=False)
    if completed.returncode:
        raise ValidationError('pip failed inside the dedicated environment: ' + completed.stderr[-3000:])
    return {**plan, 'returncode': completed.returncode, 'next_step': f'Install your AlFarouq checkout/wheel using {plan["command"][0]} -m pip install <path-to-checkout-or-wheel>, then select that interpreter in VS Code.'}
