"""Ollama HTTP contract tests against a local stub, NOT actual LLM inference."""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import pytest
from alfarouqai import Client, Config, ConsentRequired, ValidationError
from alfarouqai.providers import ollama_request


def test_network_off_by_default():
    with pytest.raises(ConsentRequired,match='Network disabled'):
        Client(Config(model='test-local')).run('llm.chat',prompt='hello')


def test_remote_requires_second_consent():
    config=Config(model='test-local',allow_network=True,ollama_url='https://example.org')
    with pytest.raises(ConsentRequired,match='Remote origin'):
        ollama_request(config,'/api/chat',{})


@pytest.mark.parametrize('url',['file:///etc/passwd','http://user:secret@127.0.0.1:11434','http://127.0.0.1:11434/path','http://127.0.0.1:11434?query=x'])
def test_unsafe_origin(url):
    config=Config(model='test-local',allow_network=True,ollama_url=url)
    with pytest.raises(ValidationError): ollama_request(config,'/api/chat',{})


def test_remote_http_rejected():
    config=Config(model='test-local',allow_network=True,allow_remote=True,ollama_url='http://example.org')
    with pytest.raises(ValidationError): ollama_request(config,'/api/chat',{})


def test_cloud_suffix_rejected():
    with pytest.raises(ValidationError):
        ollama_request(Config(model='test-cloud',allow_network=True),'/api/chat',{})


@pytest.mark.contract
def test_local_http_contract():
    received=[]
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            received.append((self.path,payload))
            raw=json.dumps({'model':'contract-stub','message':{'content':'transport-contract-only'},'done':True}).encode()
            self.send_response(200); self.send_header('Content-Length',str(len(raw)))
            self.end_headers(); self.wfile.write(raw)
        def log_message(self,*args): pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    worker=threading.Thread(target=server.serve_forever,daemon=True); worker.start()
    try:
        client=Client(Config(model='contract-stub',allow_network=True,ollama_url=f'http://127.0.0.1:{server.server_port}'))
        result=client.run('llm.chat',prompt='private fixture')
        assert result.data['text']=='transport-contract-only'
        assert received[0][0]=='/api/chat'
        assert received[0][1]['stream'] is False
        assert received[0][1]['messages'][0]['content']=='private fixture'
    finally:
        server.shutdown(); server.server_close(); worker.join()


@pytest.mark.contract
def test_redirect_is_not_followed():
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            self.send_response(307); self.send_header('Location','http://example.org/leak'); self.end_headers()
        def log_message(self,*args): pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    worker=threading.Thread(target=server.serve_forever,daemon=True); worker.start()
    try:
        with pytest.raises(ConsentRequired,match='redirects'):
            ollama_request(Config(model='contract-stub',allow_network=True,ollama_url=f'http://127.0.0.1:{server.server_port}'),'/api/chat',{})
    finally:
        server.shutdown(); server.server_close(); worker.join()
