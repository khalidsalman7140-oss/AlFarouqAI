# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Opt-in local Ollama transport. No network calls on import."""
from __future__ import annotations
import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from .core import AlFarouqError, ConsentRequired, Result, ValidationError, input_file


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ConsentRequired('HTTP redirects are disabled; configure the intended endpoint explicitly')


def ollama_request(config, endpoint, payload):
    if not config.allow_network:
        raise ConsentRequired('Network disabled, including localhost. Set Config(allow_network=True) to contact your Ollama server.')
    parsed = urllib.parse.urlsplit(config.ollama_url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ('', '/'):
        raise ValidationError('Ollama URL must be a clean http(s) origin without credentials or path')
    if parsed.hostname not in ('localhost', '127.0.0.1', '::1'):
        if not config.allow_remote:
            raise ConsentRequired('Remote origin disabled. Explicit allow_remote=True is required to send inputs outside loopback.')
        if parsed.scheme != 'https':
            raise ValidationError('Remote Ollama connections require HTTPS')
    if not config.model or config.model.endswith('-cloud'):
        raise ValidationError('An explicitly chosen locally installed model is required; -cloud model suffix is blocked')
    raw = json.dumps(payload, ensure_ascii=False).encode()
    if len(raw) > config.max_input_bytes*2:
        raise ValidationError('Request exceeds budget')
    request = urllib.request.Request(config.ollama_url.rstrip('/') + endpoint, data=raw, headers={'Content-Type': 'application/json'})
    # Disable environment proxy discovery: local/private text must not leak to a proxy.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(request, timeout=config.timeout) as response:
            content = response.read(config.max_input_bytes+1)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise AlFarouqError(f'Ollama request failed: {type(exc).__name__}; verify server, model and timeout') from exc
    if len(content) > config.max_input_bytes:
        raise ValidationError('Response exceeds budget')
    try:
        return json.loads(content)
    except (ValueError, UnicodeError) as exc:
        raise ValidationError('Ollama response is not valid JSON') from exc


def chat(*, prompt, config, system=None, image=None, **kwargs):
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValidationError('Nonempty prompt required')
    messages = []
    if system:
        messages.append({'role': 'system', 'content': system})
    message = {'role': 'user', 'content': prompt}
    if image:
        p = input_file(image, config)
        message['images'] = [base64.b64encode(p.read_bytes()).decode('ascii')]
    messages.append(message)
    response = ollama_request(config, '/api/chat', {'model': config.model, 'messages': messages, 'stream': False, 'options': {'temperature': 0}})
    if not isinstance(response.get('message'), dict) or not isinstance(response['message'].get('content'), str):
        raise ValidationError('Ollama response missing message.content')
    return Result('llm.chat', {'text': response['message']['content'], 'model': response.get('model', config.model), 'done': response.get('done')}, 'ollama', ['Generated content may be incorrect. Verify citations and code. Ollama must be configured to avoid cloud-backed aliases.'], {'endpoint': config.ollama_url, 'model': config.model})
