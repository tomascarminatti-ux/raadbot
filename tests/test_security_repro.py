import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_refine_gem_path_traversal():
    # Attempt path traversal in gem_id
    payload = {
        "gem_id": "../config",
        "instruction": "test"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    # Pydantic validation should catch this and return 422
    assert response.status_code == 422

def test_setup_search_path_traversal():
    payload = {
        "search_id": "valid_id/../traversal",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422

def test_run_pipeline_path_traversal():
    payload = {
        "search_id": "../../etc/passwd",
        "local_dir": "./inputs"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_valid_ids():
    # Mocking files/env might be needed for full success,
    # but here we just test that valid IDs PASS validation (not necessarily 200 if other things fail)
    payload = {
        "gem_id": "gem1",
        "instruction": "test"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    # It should NOT be 422. Might be 404 or 500 depending on environment/API keys
    assert response.status_code != 422
