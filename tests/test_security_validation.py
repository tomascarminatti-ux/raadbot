import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from api import app

client = TestClient(app)

def test_refine_gem_validation():
    # Valid gem_id - we only check if it PASSES Pydantic (not 422)
    with patch("agent.gemini_client.GeminiClient.run_gem") as mock_run:
        mock_run.return_value = {"markdown": "new prompt"}
        response = client.post("/api/v1/gems/refine", json={"gem_id": "gem1", "instruction": "test"})
        assert response.status_code != 422

    # Invalid gem_id (path traversal attempt)
    response = client.post("/api/v1/gems/refine", json={"gem_id": "../config", "instruction": "test"})
    assert response.status_code == 422
    assert "Invalid gem_id" in response.text

def test_pipeline_request_validation():
    # Valid search_id
    response = client.post("/api/v1/run", json={"search_id": "valid-id_123", "local_dir": "."})
    assert response.status_code != 422

    # Invalid search_id
    response = client.post("/api/v1/run", json={"search_id": "invalid;id", "local_dir": "."})
    assert response.status_code == 422
    assert "Invalid search_id" in response.text
