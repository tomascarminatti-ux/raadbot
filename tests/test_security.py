from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_pipeline_request_path_traversal_search_id():
    # Test path traversal in search_id
    payload = {"search_id": "../etc/passwd", "local_dir": "runs/test"}
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Identifier must only contain alphanumeric characters" in response.text


def test_pipeline_request_path_traversal_candidate_id():
    # Test path traversal in candidate_id
    payload = {
        "search_id": "valid-id",
        "candidate_id": "nested/path",
        "local_dir": "runs/test",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Identifier must only contain alphanumeric characters" in response.text


def test_pipeline_request_path_traversal_local_dir():
    # Test path traversal in local_dir
    payload = {"search_id": "valid-id", "local_dir": "../../etc/passwd"}
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Directory traversal or absolute paths are not allowed" in response.text


def test_pipeline_request_absolute_local_dir():
    # Test absolute path in local_dir
    payload = {"search_id": "valid-id", "local_dir": "/etc/passwd"}
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Directory traversal or absolute paths are not allowed" in response.text


def test_setup_search_path_traversal():
    # Test path traversal in SetupSearchRequest search_id
    payload = {"search_id": "invalid/id", "brief_notes": "notes", "jd_content": "jd"}
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "Identifier must only contain alphanumeric characters" in response.text


def test_refine_gem_path_traversal():
    # Test path traversal in RefineRequest gem_id
    payload = {"gem_id": "../api", "instruction": "Make it better"}
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "GEM ID must only contain alphanumeric characters" in response.text


def test_valid_requests_schema_validation():
    # Verify that a valid request passes Pydantic validation (it might still fail downstream due to missing files/keys, which is expected)
    payload = {"search_id": "valid_id-123", "local_dir": "runs/test"}
    # This shouldn't raise a 422, but might raise 400 (from run_pipeline raise ValueError / HTTPException)
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code != 422
