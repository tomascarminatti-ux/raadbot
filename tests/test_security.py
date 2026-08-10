from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_pipeline_request_search_id_traversal():
    """Verify that search_id in PipelineRequest rejects path traversal and invalid characters."""
    # Test case 1: Traversal sequence
    response = client.post(
        "/api/v1/run", json={"search_id": "../invalid-id", "local_dir": "runs/valid"}
    )
    assert response.status_code == 422
    assert "Identifier must be alphanumeric" in response.text

    # Test case 2: Invalid characters
    response = client.post(
        "/api/v1/run",
        json={"search_id": "search/id/with/slashes", "local_dir": "runs/valid"},
    )
    assert response.status_code == 422
    assert "Identifier must be alphanumeric" in response.text


def test_pipeline_request_candidate_id_traversal():
    """Verify that candidate_id in PipelineRequest rejects path traversal and invalid characters."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_search_id",
            "candidate_id": "../../bad_candidate",
            "local_dir": "runs/valid",
        },
    )
    assert response.status_code == 422
    assert "Identifier must be alphanumeric" in response.text


def test_pipeline_request_local_dir_traversal():
    """Verify that local_dir in PipelineRequest rejects traversal sequences and absolute paths."""
    # Test directory traversal with ..
    response = client.post(
        "/api/v1/run", json={"search_id": "valid_search", "local_dir": "runs/../../etc"}
    )
    assert response.status_code == 422
    assert "Directory traversal is not allowed" in response.text

    # Test absolute paths
    response = client.post(
        "/api/v1/run", json={"search_id": "valid_search", "local_dir": "/etc/passwd"}
    )
    assert response.status_code == 422
    assert "Absolute paths are not allowed" in response.text

    # Test drive letters
    response = client.post(
        "/api/v1/run", json={"search_id": "valid_search", "local_dir": "C:/Windows"}
    )
    assert response.status_code == 422
    assert "Absolute paths are not allowed" in response.text


def test_setup_search_request_search_id_traversal():
    """Verify that SetupSearchRequest search_id rejects traversal sequences."""
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "invalid/id",
            "brief_notes": "some notes",
            "jd_content": "some jd",
        },
    )
    assert response.status_code == 422
    assert "search_id must be alphanumeric" in response.text


def test_refine_request_gem_id_traversal():
    """Verify that RefineRequest gem_id rejects traversal sequences."""
    response = client.post(
        "/api/v1/gems/refine", json={"gem_id": "../../gem5", "instruction": "refine it"}
    )
    assert response.status_code == 422
    assert "gem_id must be alphanumeric" in response.text
