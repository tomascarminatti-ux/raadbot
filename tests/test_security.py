import pytest
from fastapi.testclient import TestClient
import os
from api import app

client = TestClient(app)

def test_refine_gem_path_traversal():
    """Test that gem_id is validated to prevent path traversal."""
    payload = {
        "gem_id": "../hacked",
        "instruction": "Do something bad"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    # If the fix is not applied, it might return 404 (file not found) but still attempt to use the path.
    # After fix, it should return 422 Unprocessable Entity due to Pydantic validation.
    assert response.status_code == 422

def test_trigger_pipeline_path_traversal():
    """Test that search_id and local_dir are validated to prevent path traversal."""
    # Test search_id traversal
    payload = {
        "search_id": "../../evil",
        "local_dir": "runs/SEARCH-TEST-001/inputs"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

    # Test local_dir traversal (absolute path)
    payload = {
        "search_id": "valid-id",
        "local_dir": "/etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

    # Test local_dir traversal (parent directory)
    payload = {
        "search_id": "valid-id",
        "local_dir": "../../../"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_setup_search_path_traversal():
    """Test that search_id in setup_search is validated."""
    payload = {
        "search_id": "sub/folder",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
