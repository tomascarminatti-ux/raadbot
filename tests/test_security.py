import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_pipeline_run_path_traversal():
    # Test search_id path traversal
    response = client.post("/api/v1/run", json={
        "search_id": "../../etc/passwd",
        "local_dir": "runs"
    })
    assert response.status_code == 422
    assert "Possible path traversal detected." in response.text

    # Test local_dir path traversal (absolute Unix path)
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "/etc"
    })
    assert response.status_code == 422
    assert "Possible path traversal detected." in response.text

    # Test local_dir path traversal (Windows drive letter)
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "C:\\Windows"
    })
    assert response.status_code == 422
    assert "Possible path traversal detected." in response.text

def test_pipeline_run_ssrf():
    # Test webhook_url SSRF with localhost
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "runs",
        "webhook_url": "http://localhost:8000/health"
    })
    assert response.status_code == 422
    assert "Webhook URL contains forbidden hostname" in response.text

    # Test webhook_url SSRF with private IP
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "runs",
        "webhook_url": "http://192.168.1.1/api"
    })
    assert response.status_code == 422
    assert "Webhook URL contains forbidden hostname" in response.text

    # Test webhook_url with legitimate URL containing '10.' but not as hostname
    # This should now PASS because we use urlparse.hostname
    # But wait, we don't have a mock for the pipeline run, so it might fail with 400 (Value error GEMINI_API_KEY)
    # But the VALIDATION (Pydantic) should pass.
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "runs",
        "webhook_url": "https://api.service.com/v10.1/webhook"
    })
    # If Pydantic validation passes, it proceeds to run_pipeline.
    # Since we don't have a real API key or inputs, it will fail later,
    # but NOT with 422 (validation error).
    assert response.status_code != 422

def test_search_setup_path_traversal():
    response = client.post("/api/v1/search/setup", json={
        "search_id": "../traversal",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422
    assert "Possible path traversal detected." in response.text

def test_gem_refine_path_traversal():
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../test",
        "instruction": "refine"
    })
    assert response.status_code == 422
    assert "Possible path traversal detected." in response.text
