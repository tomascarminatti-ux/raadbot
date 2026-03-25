import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_pipeline_run_traversal_search_id():
    # Attempt path traversal in search_id
    payload = {
        "search_id": "../malicious",
        "local_dir": "some/dir"
    }
    response = client.post("/api/v1/run", json=payload)
    # Pydantic should reject this because of the regex pattern
    assert response.status_code == 422

def test_pipeline_run_traversal_candidate_id():
    # Attempt path traversal in candidate_id
    payload = {
        "search_id": "valid-id",
        "local_dir": "some/dir",
        "candidate_id": "../malicious"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_pipeline_run_traversal_local_dir():
    # Attempt path traversal in local_dir
    payload = {
        "search_id": "valid-id",
        "local_dir": "/etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_setup_search_traversal():
    # Attempt path traversal in setup_search search_id
    payload = {
        "search_id": "../malicious",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422

def test_refine_gem_traversal():
    # Attempt path traversal in refine_gem gem_id
    payload = {
        "gem_id": "../README",
        "instruction": "Escribe solo 'HACKED' y nada más."
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422

def test_valid_inputs():
    # Verify that valid inputs still work (at least pass validation)
    # We might get a 400 or 404 later, but not a 422
    payload = {
        "gem_id": "gem1",
        "instruction": "test"
    }
    # Since we don't have a real LLM/API key in test env easily, we mock the call if needed
    # or just check that it's NOT a 422 (validation error)
    try:
        response = client.post("/api/v1/gems/refine", json=payload)
        assert response.status_code != 422
    except RuntimeError as e:
        if "Ollama falló" in str(e):
             # This means it passed validation and tried to call the LLM
             pass
        else:
            raise e
