# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Dependency-free text, CSV, source-code, defensive log and sensor analytics."""
from __future__ import annotations
import ast
import csv
import math
import re
import statistics
from collections import Counter
from pathlib import Path
from .core import Config, Result, ValidationError, fingerprint, input_file


def tokens(text):
    return re.findall(r'[^\W_]+', text.casefold(), re.UNICODE)


def text_analyze(*, text, config: Config, **kwargs):
    if not isinstance(text, str) or len(text.encode('utf-8')) > config.max_input_bytes:
        raise ValidationError('Text must be a string within the input limit')
    words = tokens(text)
    sentences = [s.strip() for s in re.split(r'(?<=[.!?؟])\s+|\n+', text) if s.strip()]
    stop = set('the a an is are to of in and or for this that with على في من إلى عن هذا هذه هو هي و أو'.split())
    freq = Counter(w for w in words if w not in stop and len(w) > 1)
    scored = [(sum(freq[w] for w in tokens(s)) / max(1, len(tokens(s))), i, s) for i, s in enumerate(sentences)]
    selected = sorted(sorted(scored, key=lambda x: (-x[0], x[1]))[:3], key=lambda x: x[1])
    return Result('text.analyze', {'characters': len(text), 'words': len(words), 'sentences': len(sentences), 'keywords': freq.most_common(12), 'extractive_summary': ' '.join(x[2] for x in selected)}, 'stdlib.frequency', ['Extractive statistics only; not an LLM or sentiment model.'])


def read_csv(data, config):
    p = input_file(data, config)
    with p.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValidationError('CSV needs a header with unique columns')
        rows = []
        for row in reader:
            if len(rows) >= config.max_rows:
                raise ValidationError('CSV exceeds max_rows')
            if None in row or any(v is None for v in row.values()):
                raise ValidationError('Malformed CSV: row length differs from header')
            rows.append(row)
    if not rows:
        raise ValidationError('CSV contains no data rows')
    return p, rows


def finite_number(value):
    try:
        v = float(value)
        return v if math.isfinite(v) else None
    except (ValueError, TypeError):
        return None


def data_profile(*, data, config, **kwargs):
    p, rows = read_csv(data, config)
    columns = {}
    for col in rows[0]:
        values = [r[col] for r in rows]
        present = [v for v in values if v.strip()]
        numbers = [finite_number(v) for v in present]
        numeric = bool(present) and all(v is not None for v in numbers)
        item = {'missing': len(values) - len(present), 'unique': len(set(present)), 'type': 'numeric' if numeric else 'text'}
        if numeric:
            item.update({'min': min(numbers), 'max': max(numbers), 'mean': statistics.mean(numbers), 'stdev': statistics.stdev(numbers) if len(numbers) > 1 else 0})
        columns[col] = item
    return Result('data.profile', {'row_count': len(rows), 'columns': columns, 'rows': rows[:5]}, 'stdlib.csv', provenance={'input_sha256': fingerprint(p), 'preview_only': True})


def sensor_analyze(*, data, column, threshold=3.0, config, **kwargs):
    p, rows = read_csv(data, config)
    if column not in rows[0] or finite_number(threshold) is None or float(threshold) <= 0:
        raise ValidationError('Need existing numeric column and threshold > 0')
    vals = [finite_number(r[column]) for r in rows]
    if any(v is None for v in vals):
        raise ValidationError('Sensor series must contain only finite numbers')
    if len(vals) < 3:
        raise ValidationError('At least three observations required')
    mean, std = statistics.mean(vals), statistics.pstdev(vals)
    scored = [{'row': i, 'value': v, 'z_score': (v-mean)/std if std else 0.0, 'anomaly': abs(v-mean)/std > float(threshold) if std else False} for i, v in enumerate(vals)]
    return Result('iot.analyze', {'mean': mean, 'std': std, 'threshold': float(threshold), 'rows': scored}, 'stdlib.zscore', ['Offline sensor analytics; no device is connected and no actuator commands are sent.'], {'input_sha256': fingerprint(p)})


class SourceVisitor(ast.NodeVisitor):
    def __init__(self, name):
        self.name = name
        self.imports = set()
        self.findings = []
        self.functions = []
        self.classes = []
        self.aliases = {}

    def add(self, node, rule, message):
        self.findings.append({'file': self.name, 'line': node.lineno, 'rule': rule, 'message': message})

    def visit_Import(self, node):
        for item in node.names:
            self.imports.add(item.name)
            self.aliases[item.asname or item.name] = item.name

    def visit_ImportFrom(self, node):
        self.imports.add(node.module or '')
        for item in node.names:
            self.aliases[item.asname or item.name] = f'{node.module}.{item.name}'

    def visit_FunctionDef(self, node):
        self.functions.append({'name': node.name, 'line': node.lineno, 'documented': bool(ast.get_docstring(node)), 'branches': sum(isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.IfExp)) for n in ast.walk(node))})
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        self.classes.append({'name': node.name, 'line': node.lineno})
        self.generic_visit(node)

    def visit_Call(self, node):
        def full(n):
            if isinstance(n, ast.Name):
                return self.aliases.get(n.id, n.id)
            if isinstance(n, ast.Attribute):
                return full(n.value) + '.' + n.attr
            return ''
        name = full(node.func)
        if name in ('eval', 'exec', 'os.system', 'pickle.load', 'pickle.loads', 'yaml.load'):
            self.add(node, 'dangerous-call', f'Review {name}; untrusted input may execute code')
        if name.startswith('subprocess.') and any(k.arg == 'shell' and isinstance(k.value, ast.Constant) and k.value.value is True for k in node.keywords):
            self.add(node, 'shell-true', 'shell=True can enable command injection')
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.type is None:
            self.add(node, 'bare-except', 'Bare except hides interrupts and failures')
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and re.search(r'(password|secret|api_key|token)$', target.id, re.I) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str) and node.value.value:
                self.add(node, 'possible-secret', 'Possible hard-coded credential (value redacted)')
        self.generic_visit(node)


def code_analyze(*, path=None, code=None, config, **kwargs):
    if (path is None) == (code is None):
        raise ValidationError('Provide exactly one of code= or path=')
    sources = []
    if code is not None:
        if len(code.encode()) > config.max_input_bytes:
            raise ValidationError('Code input too large')
        sources.append(('<inline>', code))
    else:
        p = Path(path)
        if p.is_symlink():
            raise ValidationError('Symlink root not accepted')
        candidates = [p] if p.is_file() else sorted(p.rglob('*.py')) if p.is_dir() else []
        total = 0
        for f in candidates:
            if any(part in {'.git', '.venv', 'venv', '__pycache__', 'node_modules', 'build', 'dist'} for part in f.parts) or f.is_symlink():
                continue
            input_file(f, config)
            total += f.stat().st_size
            if len(sources) >= 1000 or total > config.max_input_bytes:
                raise ValidationError('Project exceeds 1000 files or byte budget')
            sources.append((str(f.relative_to(p)) if p.is_dir() else f.name, f.read_text(encoding='utf-8-sig')))
        if not sources:
            raise ValidationError('No Python source files found')
    rows, findings = [], []
    for name, source in sources:
        try:
            tree = ast.parse(source, filename=name)
        except SyntaxError as exc:
            findings.append({'file': name, 'line': exc.lineno, 'rule': 'syntax-error', 'message': exc.msg})
            continue
        visitor = SourceVisitor(name)
        visitor.visit(tree)
        rows.append({'file': name, 'lines': len(source.splitlines()), 'imports': sorted(visitor.imports), 'functions': visitor.functions, 'classes': visitor.classes})
        findings.extend(visitor.findings)
    return Result('code.analyze', {'parsed_files': len(rows), 'rows': rows, 'findings': findings}, 'stdlib.ast', ['Static heuristic review; not a proof of security. Source code was not executed.'])


def security_logs(*, path, config, **kwargs):
    p = input_file(path, config)
    counts = Counter()
    events = []
    for i, line in enumerate(p.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
        if re.search(r'failed password|authentication failure|invalid user|login failed', line, re.I):
            ip = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
            host = ip.group() if ip else 'unknown'
            counts[host] += 1
            events.append({'line': i, 'rule': 'authentication-failure', 'source': host})
    return Result('security.logs', {'rows': events, 'failed_auth_by_source': dict(counts)}, 'stdlib.rules', ['Defensive, offline heuristic analysis only; no network scanning or exploitation.'])
