import pytest
from fastapi.testclient import TestClient
import config

# Set dummy GEMINI_API_KEY for tests
config.GEMINI_API_KEY = "dummy_test_key"

from api import app

client = TestClient(app)

def test_pipeline_request_search_id_validation():
    # Invalid search_id with directory traversal
    response = client.post("/api/v1/run", json={
        "search_id": "../invalid-id",
        "local_dir": "runs/test"
    })
    assert response.status_code == 422
    assert "search_id" in response.text

    # Invalid search_id with spaces or special characters
    response = client.post("/api/v1/run", json={
        "search_id": "invalid id!",
        "local_dir": "runs/test"
    })
    assert response.status_code == 422
    assert "search_id" in response.text

    # Valid search_id but no other requirements (should raise 400 ValueError instead of 422 ValidationError if it reaches run_pipeline)
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id-123"
    })
    # Since search_id is valid, it proceeds to run_pipeline, which raises ValueError because neither drive_folder nor local_dir are set.
    # This results in a 400 Bad Request.
    assert response.status_code == 400
    assert "Se debe proveer" in response.text


def test_pipeline_request_candidate_id_validation():
    # Invalid candidate_id
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "runs/test",
        "candidate_id": "invalid/candidate"
    })
    assert response.status_code == 422
    assert "candidate_id" in response.text


def test_pipeline_request_local_dir_validation():
    # Invalid local_dir with path traversal
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "../../etc"
    })
    assert response.status_code == 422
    assert "local_dir" in response.text

    # Invalid local_dir with absolute path
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "/etc/passwd"
    })
    assert response.status_code == 422
    assert "local_dir" in response.text


def test_setup_search_validation():
    # Invalid search_id with traversal
    response = client.post("/api/v1/search/setup", json={
        "search_id": "some/path/../id",
        "brief_notes": "notes",
        "jd_content": "jd"
    })
    assert response.status_code == 422
    assert "search_id" in response.text


def test_refine_gem_validation():
    # Invalid gem_id (not gem1 - gem5)
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem6",
        "instruction": "refine"
    })
    assert response.status_code == 422
    assert "gem_id" in response.text

    # Attempted traversal on gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../../api",
        "instruction": "refine"
    })
    assert response.status_code == 422
    assert "gem_id" in response.text
