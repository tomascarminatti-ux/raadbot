import os

# Set a dummy API key for startup check before importing app
os.environ["GEMINI_API_KEY"] = "dummy"

import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_refine_gem_blocked():
    # Attempt to refine it via gem_id path traversal
    payload = {
        "gem_id": "../vulnerable_test",
        "instruction": "Overwrite with malicious content"
    }

    response = client.post("/api/v1/gems/refine", json=payload)
    # Should be blocked by Pydantic validation (422)
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

def test_path_traversal_run_pipeline_search_id_blocked():
    payload = {
        "search_id": "../evil_run_dir",
        "local_dir": "prompts"
    }

    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

def test_ssrf_protection_webhook_url():
    # Localhost SSRF
    payload = {
        "search_id": "test_search",
        "local_dir": "runs",
        "webhook_url": "http://localhost:8000/api/v1/run"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Localhost or loopback addresses are not allowed" in response.text

    # Loopback IP SSRF
    payload["webhook_url"] = "http://127.0.0.1:8000"
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Localhost or loopback addresses are not allowed" in response.text

    # Valid external URL should pass validation (but might fail later)
    payload["webhook_url"] = "https://n8n.example.com/webhook"
    response = client.post("/api/v1/run", json=payload)
    # Since we use background tasks, it should return 200 or 400 depending on run_pipeline
    # But validation passed
    assert response.status_code != 422

def test_path_traversal_run_pipeline_local_dir_blocked():
    # Absolute path
    payload = {
        "search_id": "test_search",
        "local_dir": "/etc"
    }

    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

    # Parent directory traversal
    payload = {
        "search_id": "test_search",
        "local_dir": "runs/../../etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

def test_path_traversal_candidate_id_blocked():
    payload = {
        "search_id": "test_search",
        "local_dir": "runs",
        "candidate_id": "../evil"
    }

    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text
