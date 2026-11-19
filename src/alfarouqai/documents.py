# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Text extraction, lexical retrieval and optional local semantic retrieval."""
from __future__ import annotations
import json
import math
import re
import zipfile
from collections import Counter
from pathlib import Path
from .core import Result, ValidationError, require, input_file, atomic_write, ConsentRequired, fingerprint
from .local import tokens


def document_read(*, document, config, **kwargs):
    p = input_file(document, config)
    ext = p.suffix.lower()
    rows, text = [], ''
    if ext in ('.docx', '.xlsx'):
        try:
            with zipfile.ZipFile(p) as archive:
                if sum(info.file_size for info in archive.infolist()) > config.max_input_bytes * 5:
                    raise ValidationError('Office archive expansion budget exceeded')
        except zipfile.BadZipFile as exc:
            raise ValidationError('Invalid Office ZIP container') from exc
    if ext in ('.txt', '.md', '.csv', '.json', '.py', '.log'):
        text = p.read_text(encoding='utf-8-sig')
        backend = 'stdlib.text'
    elif ext == '.pdf':
        pdf = require('pypdf', 'documents')
        reader = pdf.PdfReader(str(p))
        if reader.is_encrypted:
            raise ValidationError('Encrypted PDF must be unlocked outside this adapter')
        if len(reader.pages) > 500:
            raise ValidationError('PDF page limit is 500')
        total = 0
        for i, page in enumerate(reader.pages, 1):
            t = page.extract_text() or ''
            total += len(t.encode())
            if total > config.max_input_bytes:
                raise ValidationError('Extracted text exceeds byte budget')
            rows.append({'page': i, 'text': t})
        text = '\n'.join(r['text'] for r in rows)
        backend = 'pypdf'
    elif ext == '.docx':
        docx = require('docx', 'documents')
        doc = docx.Document(str(p))
        parts = [para.text for para in doc.paragraphs]
        parts += ['\t'.join(c.text for c in row.cells) for table in doc.tables for row in table.rows]
        text, backend = '\n'.join(parts), 'python-docx'
    elif ext == '.xlsx':
        xl = require('openpyxl', 'documents')
        book = xl.load_workbook(str(p), read_only=True, data_only=True)
        total_cells = 0
        try:
            for sheet in book:
                for row in sheet.iter_rows(values_only=True):
                    total_cells += len(row)
                    if len(rows) >= config.max_rows or total_cells > 1_000_000:
                        raise ValidationError('Spreadsheet row/cell limit exceeded')
                    rows.append({'sheet': sheet.title, 'values': [str(c) if c is not None else '' for c in row]})
        finally:
            book.close()
        text, backend = '\n'.join('\t'.join(r['values']) for r in rows), 'openpyxl'
    else:
        raise ValidationError('Supported inputs: txt md csv json py log pdf docx xlsx')
    if len(text.encode()) > config.max_input_bytes:
        raise ValidationError('Extracted text exceeds budget')
    return Result('document.read', {'text': text, 'characters': len(text), 'rows': rows}, backend, ['Text extraction only; scanned PDFs need OCR, formulas are not recalculated, complex layout may be lost.'], {'input_sha256': fingerprint(p)})


class KnowledgeBase:
    """Bounded lexical TF-IDF/cosine search. Stored documents are data, not commands."""
    def __init__(self, *, chunk_size=800, overlap=100, max_characters=5_000_000):
        if chunk_size < 40 or not 0 <= overlap < chunk_size:
            raise ValidationError('chunk_size >=40 and 0 <= overlap < chunk_size required')
        self.chunk_size, self.overlap = chunk_size, overlap
        self.max_characters = max_characters
        self.chunks = []

    def add(self, text, *, source='inline'):
        if not isinstance(text, str) or len(text) + sum(len(x['text']) for x in self.chunks) > self.max_characters:
            raise ValidationError('Knowledge base character budget exceeded')
        if not text.strip():
            raise ValidationError('Cannot index empty text')
        count = 0
        for start in range(0, len(text), self.chunk_size - self.overlap):
            content = text[start:start+self.chunk_size]
            self.chunks.append({'id': len(self.chunks), 'source': str(source), 'start': start, 'end': start + len(content), 'text': content})
            count += 1
            if start + self.chunk_size >= len(text):
                break
        return count

    def search(self, query, *, k=4):
        if not query.strip() or not isinstance(k, int) or k < 1 or k > 100:
            raise ValidationError('Nonempty query and 1 <= k <= 100 required')
        counts = [Counter(tokens(c['text'])) for c in self.chunks]
        query_counts = Counter(tokens(query))
        n = len(counts)
        vocab = set(query_counts)
        for cnt in counts:
            vocab.update(cnt)
        idf = {t: math.log((1+n)/(1+sum(t in c for c in counts)))+1 for t in vocab}
        def vec(c):
            raw = {t: (1+math.log(v))*idf[t] for t, v in c.items()}
            norm = math.sqrt(sum(v*v for v in raw.values())) or 1
            return {t: v/norm for t, v in raw.items()}
        q = vec(query_counts)
        ranked = []
        for chunk, cnt in zip(self.chunks, counts):
            v = vec(cnt)
            score = sum(value*v.get(t, 0) for t, value in q.items())
            if score > 0:
                ranked.append({**chunk, 'score': score})
        ranked.sort(key=lambda r: (-r['score'], r['id']))
        return Result('rag.search', {'query': query, 'rows': ranked[:k]}, 'stdlib.lexical-tfidf-cosine', ['Lexical retrieval, not semantic embeddings. No generated answer was fabricated.'])

    def save(self, path):
        return atomic_write(path, json.dumps({'format': 'alfarouq.lexical.v1', 'chunk_size': self.chunk_size, 'overlap': self.overlap, 'chunks': self.chunks}, ensure_ascii=False))

    @classmethod
    def load(cls, path, *, config=None):
        from .core import Config
        p = input_file(path, config or Config())
        data = json.loads(p.read_text(encoding='utf-8'))
        if data.get('format') != 'alfarouq.lexical.v1':
            raise ValidationError('Unsupported knowledge base format')
        obj = cls(chunk_size=data['chunk_size'], overlap=data['overlap'])
        chunks = data.get('chunks')
        if not isinstance(chunks, list) or len(chunks) > 100_000:
            raise ValidationError('Invalid chunks')
        if any(not isinstance(c, dict) or not isinstance(c.get('text'), str) or not {'id', 'source', 'start', 'end'} <= c.keys() for c in chunks):
            raise ValidationError('Invalid chunk schema')
        if sum(len(c['text']) for c in chunks) > obj.max_characters:
            raise ValidationError('Knowledge base exceeds budget')
        obj.chunks = chunks
        return obj


class SemanticIndex:
    """Optional CPU embeddings from a reviewed LOCAL SentenceTransformer model."""
    def __init__(self, model_path, *, config=None):
        from .core import Config
        self.config = config or Config()
        if not Path(model_path).is_dir():
            raise ValidationError('SemanticIndex requires a local model directory; no automatic download')
        st = require('sentence_transformers', 'semantic')
        self.model = st.SentenceTransformer(str(model_path), device='cpu', local_files_only=True, trust_remote_code=False)
        self.model_path = str(model_path)
        self.kb = KnowledgeBase()
        self.vectors = None

    def add(self, text, *, source='inline'):
        self.kb.add(text, source=source)
        self.vectors = self.model.encode([c['text'] for c in self.kb.chunks], normalize_embeddings=True)

    def search(self, query, *, k=4):
        if not query.strip() or not 1 <= k <= 100:
            raise ValidationError('Nonempty query and 1 <= k <= 100 required')
        if self.vectors is None:
            return Result('rag.semantic', {'rows': []}, 'sentence-transformers.local')
        vector = self.model.encode([query], normalize_embeddings=True)[0]
        scores = self.vectors @ vector
        best = sorted(range(len(scores)), key=lambda i: -float(scores[i]))[:k]
        return Result('rag.semantic', {'rows': [{**self.kb.chunks[i], 'score': float(scores[i])} for i in best]}, 'sentence-transformers.local', provenance={'model_path': self.model_path})
