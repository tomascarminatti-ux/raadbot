import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_pipeline_run_search_id_traversal():
    # Valid search_id should pass pydantic but might fail later (expected)
    # Invalid search_id with traversal should be rejected by pydantic (422)
    payload = {
        "search_id": "../../etc/passwd",
        "local_dir": "inputs"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_pipeline_run_local_dir_absolute():
    payload = {
        "search_id": "valid_id",
        "local_dir": "/etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_pipeline_run_local_dir_traversal():
    payload = {
        "search_id": "valid_id",
        "local_dir": "some/path/../../etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Path traversal sequence '..' not allowed" in response.text

def test_pipeline_run_candidate_id_invalid():
    payload = {
        "search_id": "valid_id",
        "local_dir": "inputs",
        "candidate_id": "invalid;id"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_setup_search_id_traversal():
    payload = {
        "search_id": "sub/folder",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422

def test_refine_gem_id_traversal():
    payload = {
        "gem_id": "gem1/../../../etc/passwd",
        "instruction": "make it better"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422

def test_valid_payload_passes_pydantic():
    # This should pass pydantic but might fail later due to missing API key or files
    # We just want to ensure it's not a 422
    payload = {
        "search_id": "SEARCH-2024-001",
        "local_dir": "runs/test/inputs"
    }
    response = client.post("/api/v1/run", json=payload)
    # 400 is returned by the endpoint if GEMINI_API_KEY is missing
    assert response.status_code in [400, 200]
