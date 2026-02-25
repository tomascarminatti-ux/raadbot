import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_search_id():
    response = client.post("/api/v1/run", json={
        "search_id": "../etc/passwd",
        "local_dir": "data/search1"
    })
    assert response.status_code == 422
    assert "Path traversal detectado" in response.text

def test_path_traversal_local_dir():
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "/absolute/path"
    })
    assert response.status_code == 422
    assert "Path traversal detectado" in response.text

def test_ssrf_webhook_url():
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "data/search1",
        "webhook_url": "http://localhost:8080/hook"
    })
    assert response.status_code == 422
    assert "SSRF detectado" in response.text

def test_ssrf_webhook_url_private_ip():
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "data/search1",
        "webhook_url": "http://192.168.1.1/hook"
    })
    assert response.status_code == 422
    assert "SSRF detectado" in response.text

def test_refine_gem_path_traversal():
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../../config.py",
        "instruction": "do something"
    })
    assert response.status_code == 422
    assert "Path traversal detectado" in response.text

def test_setup_search_path_traversal():
    response = client.post("/api/v1/search/setup", json={
        "search_id": "..//bad_path",
        "brief_notes": "notes",
        "jd_content": "jd"
    })
    assert response.status_code == 422
    assert "Path traversal detectado" in response.text

def test_valid_request_pass_validation():
    # This should still pass validation
    # We use a payload that is structurally valid but will fail in execution due to environment
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id_123",
        "local_dir": "runs/test/inputs"
    })
    # It shouldn't be 422 (validation error)
    assert response.status_code != 422
