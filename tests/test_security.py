from fastapi.testclient import TestClient
from unittest.mock import patch
from api import app

client = TestClient(app)


def test_path_traversal_search_id_setup():
    response = client.post("/api/v1/search/setup", json={
        "search_id": "../traversal",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422


def test_path_traversal_search_id_run():
    response = client.post("/api/v1/run", json={
        "search_id": "../../etc/shadow",
        "local_dir": "runs/test"
    })
    assert response.status_code == 422


def test_path_traversal_candidate_id_run():
    response = client.post("/api/v1/run", json={
        "search_id": "valid_search",
        "candidate_id": "../secret",
        "local_dir": "runs/test"
    })
    assert response.status_code == 422


def test_path_traversal_local_dir():
    traversal_paths = [
        "../secrets",
        "runs/../../etc/passwd",
        "/etc/passwd",
        "C:\\Windows\\System32",
    ]
    for path in traversal_paths:
        response = client.post("/api/v1/run", json={
            "search_id": "valid_search",
            "local_dir": path
        })
        assert response.status_code == 422


def test_gem_id_whitelist_refine():
    # Attempt path traversal
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../../etc/passwd",
        "instruction": "test"
    })
    assert response.status_code == 422

    # Attempt unauthorized file modification outside whitelist
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "arbitrary_file",
        "instruction": "test"
    })
    assert response.status_code == 422


@patch("agent.gemini_client.GeminiClient.run_gem")
def test_valid_inputs_accepted(mock_run_gem):
    mock_run_gem.return_value = {"data": {}, "markdown": "ok"}
    response = client.post("/api/v1/search/setup", json={
        "search_id": "valid-search-123",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 200
