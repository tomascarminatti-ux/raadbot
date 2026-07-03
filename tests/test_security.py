import pytest
from fastapi.testclient import TestClient
from api import app
import config

client = TestClient(app)

def test_path_traversal_run_pipeline_search_id():
    # Invalid search_id with path traversal
    payload = {
        "search_id": "../evil",
        "local_dir": "inputs"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_path_traversal_run_pipeline_local_dir():
    # Absolute path in local_dir
    payload = {
        "search_id": "valid-id",
        "local_dir": "/etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_path_traversal_run_pipeline_local_dir_traversal():
    # Traversal in local_dir
    payload = {
        "search_id": "valid-id",
        "local_dir": "inputs/../../etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_path_traversal_refine_gem_id():
    # Invalid gem_id
    payload = {
        "gem_id": "gem1/../../config",
        "instruction": "refine it"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422

def test_path_traversal_setup_search_id():
    # Invalid search_id in setup
    payload = {
        "search_id": "search_123; rm -rf /",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422

def test_valid_inputs_pass_validation(monkeypatch):
    # Mock run_pipeline to avoid actual execution
    from api import run_pipeline
    async def mock_run_pipeline(request):
        return {"status": "success", "search_id": request.search_id, "output_dir": "test", "summary": {}}

    # We need to monkeypatch the function used in the route.
    # Since trigger_pipeline calls run_pipeline, we can patch it.
    import api
    monkeypatch.setattr(api, "run_pipeline", mock_run_pipeline)

    payload = {
        "search_id": "valid-search-id_123",
        "local_dir": "inputs/folder"
    }
    response = client.post("/api/v1/run", json=payload)
    # This might still fail if other things are not mocked, but the goal is to see if it passes Pydantic
    # If it passes Pydantic, it should not be 422.
    assert response.status_code != 422
