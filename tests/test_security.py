from fastapi.testclient import TestClient
from api import app

client = TestClient(app, raise_server_exceptions=False)

def test_pipeline_request_search_id_traversal():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../etc/passwd",
            "drive_folder": "some_folder",
        }
    )
    assert response.status_code == 422

def test_pipeline_request_candidate_id_traversal():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "candidate_id": "../etc/passwd",
            "drive_folder": "some_folder",
        }
    )
    assert response.status_code == 422

def test_pipeline_request_local_dir_traversal():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "local_dir": "../../etc/passwd",
        }
    )
    assert response.status_code == 422

def test_setup_search_request_search_id_traversal():
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../etc/passwd",
            "brief_notes": "notes",
            "jd_content": "jd",
        }
    )
    assert response.status_code == 422

def test_refine_request_gem_id_traversal():
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "../etc/passwd",
            "instruction": "harden",
        }
    )
    assert response.status_code == 422

def test_pipeline_request_valid_inputs():
    # We test that valid alphanumeric strings do NOT fail Pydantic model validation.
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_search_123-id",
            "local_dir": "runs/valid-id/inputs",
        }
    )
    assert response.status_code != 422
