from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_pipeline_request_search_id_traversal():
    # Path traversal payload in search_id
    payload = {
        "search_id": "../etc",
        "local_dir": "runs"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text


def test_pipeline_request_candidate_id_traversal():
    # Path traversal payload in candidate_id
    payload = {
        "search_id": "valid-id",
        "candidate_id": "../../bin/sh",
        "local_dir": "runs"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "candidate_id" in response.text


def test_setup_search_traversal():
    payload = {
        "search_id": "subdir/../../hack",
        "brief_notes": "test notes",
        "jd_content": "test jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text


def test_refine_gem_traversal():
    payload = {
        "gem_id": "gem1/../../../etc/passwd",
        "instruction": "Make it more secure"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "gem_id" in response.text


def test_valid_ids_accepted():
    # A valid payload with clean alphanumeric/dash/underscore IDs
    # should not fail validation.
    # Note: It might return 400 or ValueError due to config keys / local_dir
    # not found, but not 422 from Pydantic validator.
    payload = {
        "search_id": "valid_search-123",
        "candidate_id": "candidate-99_abc",
        "local_dir": "nonexistent_dir"
    }
    response = client.post("/api/v1/run", json=payload)
    # Since config.GEMINI_API_KEY might not be set or nonexistent_dir is
    # missing, let's just make sure it does not return 422.
    assert response.status_code != 422
