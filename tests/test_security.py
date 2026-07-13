import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_traversal_refine():
    payload = {"gem_id": "../h", "instruction": "b"}
    assert client.post("/api/v1/gems/refine", json=payload).status_code == 422

def test_traversal_run():
    payloads = [
        {"search_id": "../../e", "local_dir": "v"},
        {"search_id": "v", "local_dir": "/etc"},
        {"search_id": "v", "local_dir": "../"}
    ]
    for p in payloads:
        assert client.post("/api/v1/run", json=p).status_code == 422

def test_traversal_setup():
    payload = {"search_id": "s/f", "brief_notes": "n", "jd_content": "j"}
    assert client.post("/api/v1/search/setup", json=payload).status_code == 422
