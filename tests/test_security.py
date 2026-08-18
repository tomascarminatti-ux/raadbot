import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_pipeline_request_path_traversal_search_id():
    response = client.post("/api/v1/run", json={
        "search_id": "../../../etc/passwd",
        "local_dir": "valid_folder"
    })
    assert response.status_code == 422
    assert "Identifier must contain only letters, numbers, underscores, or hyphens." in response.text

def test_pipeline_request_path_traversal_local_dir():
    response = client.post("/api/v1/run", json={
        "search_id": "valid_search",
        "local_dir": "../../../etc/passwd"
    })
    assert response.status_code == 422
    assert "Invalid directory path: path traversal detected." in response.text

def test_setup_search_path_traversal_search_id():
    response = client.post("/api/v1/search/setup", json={
        "search_id": "../malicious_dir",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422
    assert "search_id must contain only letters, numbers, underscores, or hyphens." in response.text

def test_refine_gem_path_traversal_gem_id():
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../gem1",
        "instruction": "refine"
    })
    assert response.status_code == 422
    assert "gem_id must contain only letters, numbers, underscores, or hyphens." in response.text
