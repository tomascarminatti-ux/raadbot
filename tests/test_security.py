import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_refine():
    payload = {"gem_id": "../hacked", "instruction": "bad"}
    assert client.post("/api/v1/gems/refine", json=payload).status_code == 422

def test_path_traversal_run():
    p1 = {"search_id": "../../evil", "local_dir": "valid"}
    assert client.post("/api/v1/run", json=p1).status_code == 422
    p2 = {"search_id": "valid", "local_dir": "/etc"}
    assert client.post("/api/v1/run", json=p2).status_code == 422
    p3 = {"search_id": "valid", "local_dir": "../"}
    assert client.post("/api/v1/run", json=p3).status_code == 422

def test_path_traversal_setup():
    payload = {"search_id": "sub/folder", "brief_notes": "n", "jd_content": "j"}
    assert client.post("/api/v1/search/setup", json=payload).status_code == 422
