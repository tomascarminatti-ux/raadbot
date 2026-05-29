import pytest
from fastapi.testclient import TestClient
from api import app
import config

client = TestClient(app)

def test_refine_gem_path_traversal():
    """Verify that path traversal in gem_id is blocked by Pydantic validation."""
    payload = {
        "gem_id": "../REPRODUCE_TRAVERSAL",
        "instruction": "Overwrite test"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    # Pydantic validation error should return 422
    assert response.status_code == 422
    assert "Invalid gem_id" in response.text

def test_refine_gem_valid_id(mocker):
    """Verify that a valid gem_id passes validation."""
    # Mock GeminiClient.run_gem to avoid actual API/Ollama calls
    mocker.patch("api.GeminiClient.run_gem", return_value={"markdown": "Refined prompt", "json": {}})

    payload = {
        "gem_id": "gem1",
        "instruction": "Test instruction"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    # 200 if prompts/gem1.md exists, 404 if it doesn't.
    # But we want to ensure it's not a 422 validation error.
    assert response.status_code in [200, 404]

def test_pipeline_run_invalid_search_id():
    """Verify that invalid search_id is blocked by ID_PATTERN."""
    payload = {
        "search_id": "invalid/id/with/slashes",
        "local_dir": "test_dir"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_pipeline_run_info_leakage():
    """Verify that generic error messages are returned instead of stack traces."""
    payload = {
        "search_id": "valid_id",
        "local_dir": "non_existent_dir"
    }
    response = client.post("/api/v1/run", json=payload)
    # This should fail in run_pipeline and be caught by the try-except in trigger_pipeline
    assert response.status_code == 400
    assert response.json()["detail"] == "Error executing pipeline. Please check parameters."
