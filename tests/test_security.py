from fastapi.testclient import TestClient
from api import app

client = TestClient(app, raise_server_exceptions=False)


def test_pipeline_request_search_id_traversal():
    """Verify that search_id with directory traversal is rejected."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../etc/passwd",
            "drive_folder": "some_folder",
        },
    )
    assert response.status_code == 422
    assert "search_id" in response.text or "validation" in response.text


def test_pipeline_request_candidate_id_traversal():
    """Verify that candidate_id with directory traversal is rejected."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "candidate_id": "../etc/passwd",
            "drive_folder": "some_folder",
        },
    )
    assert response.status_code == 422
    assert "candidate_id" in response.text or "validation" in response.text


def test_pipeline_request_local_dir_traversal():
    """Verify that local_dir with directory traversal is rejected."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "local_dir": "../../etc/passwd",
        },
    )
    assert response.status_code == 422
    assert "local_dir" in response.text or "validation" in response.text


def test_pipeline_request_local_dir_absolute():
    """Verify that local_dir starting with slash is rejected."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "local_dir": "/etc/passwd",
        },
    )
    assert response.status_code == 422


def test_setup_search_request_search_id_traversal():
    """Verify that setup search request search_id traversal is rejected."""
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../etc/passwd",
            "brief_notes": "notes",
            "jd_content": "jd",
        },
    )
    assert response.status_code == 422
    assert "search_id" in response.text or "validation" in response.text


def test_refine_request_gem_id_traversal():
    """Verify that refine request gem_id traversal is rejected."""
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "../etc/passwd",
            "instruction": "harden",
        },
    )
    assert response.status_code == 422
    assert "gem_id" in response.text or "validation" in response.text


def test_pipeline_request_valid_inputs():
    """Verify that valid alphanumeric and punctuation identifiers are accepted."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_search_123-id",
            "local_dir": "runs/valid-id/inputs",
        },
    )
    # Valid input should pass schema validation, but can fail downstream (e.g. 400 because dir does not exist),
    # but must NOT be 422 (unprocessable entity/validation error).
    assert response.status_code != 422
