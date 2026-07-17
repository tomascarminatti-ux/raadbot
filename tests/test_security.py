from fastapi.testclient import TestClient
import pytest
from api import app

client = TestClient(app, raise_server_exceptions=False)

def test_pipeline_request_path_traversal():
    # Valid characters
    payload_valid = {
        "search_id": "valid-search-123_abc",
        "local_dir": "test_dir",
        "candidate_id": "cand_1"
    }
    # Valid payload should not fail validation (might fail with 400 or other because dirs don't exist, but NOT 422)
    response = client.post("/api/v1/run", json=payload_valid)
    assert response.status_code != 422

    # Invalid search_id with directory traversal
    payload_invalid_search = {
        "search_id": "../invalid",
        "local_dir": "test_dir"
    }
    response = client.post("/api/v1/run", json=payload_invalid_search)
    assert response.status_code == 422
    assert "search_id" in response.text

    # Invalid candidate_id with directory traversal
    payload_invalid_candidate = {
        "search_id": "valid-search",
        "local_dir": "test_dir",
        "candidate_id": "../../cand"
    }
    response = client.post("/api/v1/run", json=payload_invalid_candidate)
    assert response.status_code == 422
    assert "candidate_id" in response.text


def test_setup_search_path_traversal():
    # Invalid search_id
    payload_invalid = {
        "search_id": "some/path/../id",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    response = client.post("/api/v1/search/setup", json=payload_invalid)
    assert response.status_code == 422
    assert "search_id" in response.text

    # Valid search_id
    payload_valid = {
        "search_id": "valid_search",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    response = client.post("/api/v1/search/setup", json=payload_valid)
    assert response.status_code != 422


def test_refine_gem_path_traversal():
    # Invalid gem_id
    payload_invalid = {
        "gem_id": "gem1/../../../etc/passwd",
        "instruction": "refine it"
    }
    response = client.post("/api/v1/gems/refine", json=payload_invalid)
    assert response.status_code == 422
    assert "gem_id" in response.text

    # Valid gem_id
    payload_valid = {
        "gem_id": "gem1",
        "instruction": "refine it"
    }
    response = client.post("/api/v1/gems/refine", json=payload_valid)
    assert response.status_code != 422
