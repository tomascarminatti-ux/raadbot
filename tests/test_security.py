import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app, raise_server_exceptions=False)

def test_path_traversal_run_search_id():
    payload = {
        "search_id": "../../etc/passwd",
        "local_dir": "."
    }
    response = client.post("/api/v1/run", json=payload)
    # After fix, this should be 422
    assert response.status_code == 422

def test_path_traversal_run_candidate_id():
    payload = {
        "search_id": "valid-id",
        "candidate_id": "../secret",
        "local_dir": "."
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_path_traversal_setup():
    payload = {
        "search_id": "sub/folder",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422

def test_path_traversal_refine():
    payload = {
        "gem_id": "../config",
        "instruction": "test"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422

def test_valid_inputs():
    # This might still fail with 400 or something if GEMINI_API_KEY is missing,
    # but it shouldn't be 422 due to validation.
    payload = {
        "search_id": "valid_search-123",
        "local_dir": "."
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code != 422
