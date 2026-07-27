import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app, raise_server_exceptions=False)

def test_pipeline_request_validation():
    # 1. Path traversal in search_id should be rejected with 422
    payload = {
        "search_id": "../invalid-path",
        "local_dir": "runs/test"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text

    # 2. Path traversal in candidate_id should be rejected with 422
    payload = {
        "search_id": "valid-search-id",
        "candidate_id": "../../candidate",
        "local_dir": "runs/test"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "candidate_id" in response.text

    # 3. Special characters in search_id should be rejected with 422
    payload = {
        "search_id": "invalid;sh",
        "local_dir": "runs/test"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

    # 4. Valid identifiers should pass Pydantic validation
    # (Since GEMINI_API_KEY might be missing/invalid, it might return 400/500, but not 422)
    payload = {
        "search_id": "valid_search-123",
        "local_dir": "runs/test"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code != 422


def test_setup_search_validation():
    # 1. Path traversal in search_id
    payload = {
        "search_id": "../etc/passwd",
        "brief_notes": "test notes",
        "jd_content": "test jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422

    # 2. Valid search_id
    payload = {
        "search_id": "valid-setup-id_1",
        "brief_notes": "test notes",
        "jd_content": "test jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code != 422


def test_refine_gem_validation():
    # 1. Path traversal in gem_id
    payload = {
        "gem_id": "../../etc/shadow",
        "instruction": "make it safer"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422

    # 2. Valid gem_id but not found file (should be 404, not 422)
    payload = {
        "gem_id": "nonexistent-gem-id",
        "instruction": "make it safer"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 404
