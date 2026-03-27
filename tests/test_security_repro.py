import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_pipeline_request_path_traversal_validation():
    # Attempt path traversal in search_id
    response = client.post("/api/v1/run", json={
        "search_id": "../evil",
        "local_dir": "runs"
    })
    assert response.status_code == 422
    assert "string_pattern_mismatch" in str(response.json())

    # Attempt absolute path in search_id
    response = client.post("/api/v1/run", json={
        "search_id": "/tmp/evil",
        "local_dir": "runs"
    })
    assert response.status_code == 422

def test_pipeline_request_local_dir_validation():
    # Attempt path traversal in local_dir
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "../../etc"
    })
    assert response.status_code == 422

    # Attempt absolute path in local_dir
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "/etc"
    })
    assert response.status_code == 422

def test_setup_search_path_traversal_validation():
    response = client.post("/api/v1/search/setup", json={
        "search_id": "path/traversal",
        "brief_notes": "notes",
        "jd_content": "jd"
    })
    assert response.status_code == 422

def test_refine_gem_path_traversal_validation():
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../config",
        "instruction": "infect"
    })
    assert response.status_code == 422

def test_valid_requests_pass_validation():
    # This should still fail later due to missing keys/files,
    # but it should pass Pydantic validation (422)
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id_123",
        "local_dir": "runs/subdir"
    })
    assert response.status_code != 422
