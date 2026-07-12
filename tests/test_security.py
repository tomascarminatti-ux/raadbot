import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_refine_gem_path_traversal():
    """Test that /api/v1/gems/refine is protected against path traversal."""
    payload = {
        "gem_id": "../README",
        "instruction": "Just return 'hello'"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422  # Pydantic validation error
    assert "gem_id" in response.text
    assert "Solo se permiten caracteres alfanuméricos" in response.text

def test_run_pipeline_path_traversal_ids():
    """Test that /api/v1/run is protected against path traversal in IDs."""
    payload = {
        "search_id": "bad/id",
        "local_dir": "inputs/test"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text

def test_run_pipeline_path_traversal_local_dir():
    """Test that /api/v1/run is protected against path traversal in local_dir."""
    payload = {
        "search_id": "valid-id",
        "local_dir": "../../etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "local_dir" in response.text
    assert "No se permiten rutas absolutas" in response.text

def test_setup_search_path_traversal():
    """Test that /api/v1/search/setup is protected against path traversal."""
    payload = {
        "search_id": "invalid..id",
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text
