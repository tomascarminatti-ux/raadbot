import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_search_id():
    # Attempting path traversal in search_id
    payload = {
        "search_id": "../../../etc/passwd",
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    # Before fix, this might fail with FileNotFoundError or something else,
    # but after fix it should be 422 Unprocessable Entity (due to Pydantic validation)
    assert response.status_code == 422

def test_path_traversal_run_pipeline():
    payload = {
        "search_id": "safe-id",
        "local_dir": "../../secrets",
        "drive_folder": None
    }
    # Note: local_dir isn't validated by regex yet, but it's a path.
    # However, search_id is used in os.path.join("runs", request.search_id, "outputs")

    payload_bad_id = {
        "search_id": "safe/../../../etc",
        "local_dir": "test"
    }
    response = client.post("/api/v1/run", json=payload_bad_id)
    assert response.status_code == 422

def test_gem_id_whitelist():
    payload = {
        "gem_id": "invalid_gem",
        "instruction": "make it better"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    # Should be 422 (if regex fails) or 403/404 (if whitelist fails)
    assert response.status_code in [403, 422]

def test_gem_id_path_traversal():
    payload = {
        "gem_id": "../config",
        "instruction": "make it better"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
