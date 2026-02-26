import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_security_headers():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
    assert "Content-Security-Policy" in response.headers

def test_path_traversal_protection_run():
    # Test search_id
    response = client.post("/api/v1/run", json={
        "search_id": "../etc/passwd",
        "local_dir": "data"
    })
    assert response.status_code == 422
    assert "path o ID no permitido" in response.text

    # Test local_dir
    response = client.post("/api/v1/run", json={
        "search_id": "test-search",
        "local_dir": "../../etc"
    })
    assert response.status_code == 422
    assert "path o ID no permitido" in response.text

def test_path_traversal_protection_setup():
    # Test absolute path
    response = client.post("/api/v1/search/setup", json={
        "search_id": "/etc/passwd",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422
    assert "ID no permitido" in response.text

def test_path_traversal_protection_refine():
    # Test path traversal pattern
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem1/../../config",
        "instruction": "test"
    })
    assert response.status_code == 422
    assert "GEM ID no permitido" in response.text

def test_ssrf_protection():
    # Test localhost
    response = client.post("/api/v1/run", json={
        "search_id": "test-search",
        "local_dir": "data",
        "webhook_url": "http://localhost:8080/admin"
    })
    assert response.status_code == 422
    assert "SSRF detectado" in response.text

    # Test 127.0.0.1
    response = client.post("/api/v1/run", json={
        "search_id": "test-search",
        "local_dir": "data",
        "webhook_url": "http://127.0.0.1:8000"
    })
    assert response.status_code == 422
    assert "SSRF detectado" in response.text

    # Test private IP
    response = client.post("/api/v1/run", json={
        "search_id": "test-search",
        "local_dir": "data",
        "webhook_url": "http://192.168.1.1/config"
    })
    assert response.status_code == 422
    assert "SSRF detectado" in response.text

    # Test valid external URL
    response = client.post("/api/v1/run", json={
        "search_id": "test-search",
        "local_dir": "data",
        "webhook_url": "https://hooks.n8n.io/abcd"
    })
    # It should pass Pydantic validation (422), but might fail later (400) because 'data' dir doesn't exist
    assert response.status_code != 422
