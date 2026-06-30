from fastapi.testclient import TestClient
import os

# Set environment variables for testing
os.environ["GEMINI_API_KEY"] = "fake_key_for_testing"

from api import app

client = TestClient(app)


def test_pipeline_run_path_traversal_search_id():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../traversal",
            "local_dir": "runs"
        }
    )
    assert response.status_code == 422
    assert "search_id" in response.text


def test_pipeline_run_path_traversal_local_dir():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "local_dir": "../forbidden"
        }
    )
    assert response.status_code == 422
    assert "local_dir" in response.text


def test_pipeline_run_absolute_path_local_dir():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "local_dir": "/etc/passwd"
        }
    )
    assert response.status_code == 422
    assert "local_dir" in response.text


def test_setup_search_path_traversal():
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "sub/folder",
            "brief_notes": "notes",
            "jd_content": "jd"
        }
    )
    assert response.status_code == 422
    assert "search_id" in response.text


def test_refine_gem_path_traversal():
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "gem1; rm -rf /",
            "instruction": "test"
        }
    )
    assert response.status_code == 422
    assert "gem_id" in response.text


def test_valid_requests():
    # We don't want to actually run the pipeline as it needs a real API key
    # But we can check if it passes validation
    import api

    async def mock_run_pipeline(request):
        return {"status": "mocked"}

    api.run_pipeline = mock_run_pipeline

    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id-123",
            "local_dir": "runs/test"
        }
    )
    # If it passes validation, it might still fail later because runs/test
    # doesn't exist, but it won't be a 422 validation error.
    assert response.status_code != 422
