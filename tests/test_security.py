import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app, raise_server_exceptions=False)

def test_pipeline_request_validation():
    # Valid characters should not be rejected by model validation (status may be 400 due to missing folders, but not 422)
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-search_123",
            "candidate_id": "candidate_abc",
            "local_dir": "runs/test"
        }
    )
    assert response.status_code != 422, "Valid search_id/candidate_id should not cause 422 validation error"

    # Path traversal and injection inputs
    invalid_search_ids = [
        "../traversal",
        "../../etc/passwd",
        "search;rm -rf",
        "search id with spaces",
        "search/path",
        "search?",
    ]
    for bad_id in invalid_search_ids:
        response = client.post(
            "/api/v1/run",
            json={
                "search_id": bad_id,
                "local_dir": "runs/test"
            }
        )
        assert response.status_code == 422, f"Failed to reject invalid search_id: {bad_id}"

    # Invalid candidate_id
    invalid_candidate_ids = [
        "../bad-cand",
        "cand/id",
        "cand spaces",
    ]
    for bad_cand in invalid_candidate_ids:
        response = client.post(
            "/api/v1/run",
            json={
                "search_id": "valid-search",
                "candidate_id": bad_cand,
                "local_dir": "runs/test"
            }
        )
        assert response.status_code == 422, f"Failed to reject invalid candidate_id: {bad_cand}"


def test_setup_search_validation():
    invalid_search_ids = [
        "../traversal",
        "../../etc/passwd",
        "search/path",
    ]
    for bad_id in invalid_search_ids:
        response = client.post(
            "/api/v1/search/setup",
            json={
                "search_id": bad_id,
                "brief_notes": "notes",
                "jd_content": "jd"
            }
        )
        assert response.status_code == 422, f"Failed to reject invalid search_id in setup: {bad_id}"


def test_refine_gem_validation():
    invalid_gem_ids = [
        "../traversal",
        "../../etc/passwd",
        "gem/path",
        "gem1.md",  # extension is not allowed under the regex constraint
    ]
    for bad_id in invalid_gem_ids:
        response = client.post(
            "/api/v1/gems/refine",
            json={
                "gem_id": bad_id,
                "instruction": "refine"
            }
        )
        assert response.status_code == 422, f"Failed to reject invalid gem_id: {bad_id}"
