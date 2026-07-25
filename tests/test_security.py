import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app, raise_server_exceptions=False)

def test_pipeline_request_search_id_validation():
    # Invalid search_id with path traversal
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../invalid-path",
            "drive_folder": "folder_abc"
        }
    )
    assert response.status_code == 422
    assert "search_id" in response.text

    # Invalid search_id with special characters
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "search@id",
            "drive_folder": "folder_abc"
        }
    )
    assert response.status_code == 422

    # Invalid candidate_id with path traversal
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_search_id_123",
            "candidate_id": "../bad_candidate",
            "drive_folder": "folder_abc"
        }
    )
    assert response.status_code == 422
    assert "candidate_id" in response.text


def test_setup_search_request_validation():
    # Invalid search_id with path traversal
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../../etc/passwd",
            "brief_notes": "notes",
            "jd_content": "jd"
        }
    )
    assert response.status_code == 422
    assert "search_id" in response.text


def test_refine_request_gem_id_validation():
    # Invalid gem_id with path traversal or non-whitelisted value
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "gem6",
            "instruction": "make it better"
        }
    )
    assert response.status_code == 422
    assert "gem_id" in response.text

    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "../gem1",
            "instruction": "make it better"
        }
    )
    assert response.status_code == 422
    assert "gem_id" in response.text
