import pytest
from fastapi.testclient import TestClient
from api import app
import config

client = TestClient(app)

def test_pipeline_request_validation():
    # Valid search_id
    response = client.post("/api/v1/run", json={
        "search_id": "VALID-ID-123",
        "local_dir": "runs/test"
    })
    # We expect 400 or 422?
    # If Pydantic fails, it's 422. If logic fails, it's 400.
    # In this case, local_dir might not exist, but let's check validation first.
    assert response.status_code != 422

    # Invalid search_id (path traversal)
    response = client.post("/api/v1/run", json={
        "search_id": "../invalid",
        "local_dir": "runs/test"
    })
    assert response.status_code == 422

    # Invalid candidate_id
    response = client.post("/api/v1/run", json={
        "search_id": "VALID",
        "candidate_id": "invalid; rm -rf /",
        "local_dir": "runs/test"
    })
    assert response.status_code == 422

def test_setup_search_validation(mocker):
    # Mock GeminiClient.run_gem to avoid external calls
    mocker.patch("api.GeminiClient.run_gem", return_value={"data": {}, "markdown": ""})

    # Valid
    response = client.post("/api/v1/search/setup", json={
        "search_id": "VALID",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code != 422

    # Invalid
    response = client.post("/api/v1/search/setup", json={
        "search_id": "invalid space",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422

def test_refine_gem_validation():
    # Valid
    # (Note: this might actually try to run GEM if validation passes)
    # We just care about the status code being 422 for invalid ones.

    # Invalid gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem6", # Only 1-5 allowed in config.ALLOWED_GEMS
        "instruction": "refine"
    })
    assert response.status_code == 422

    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../prompts/gem1",
        "instruction": "refine"
    })
    assert response.status_code == 422

def test_error_message_leaks():
    # Trigger an error and check if it leaks str(e)
    # We can try to run a pipeline with a non-existent local_dir
    response = client.post("/api/v1/run", json={
        "search_id": "VALID",
        "local_dir": "non-existent-dir"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Pipeline execution failed"
    assert "FileNotFoundError" not in str(response.json())
