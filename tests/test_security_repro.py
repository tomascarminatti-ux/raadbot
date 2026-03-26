import pytest
import os
import shutil
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock

# Mock config before importing app
import config
config.GEMINI_API_KEY = "dummy_key"

from api import app

client = TestClient(app)

def test_refine_gem_path_traversal_validation():
    # Now it should be blocked by Pydantic validation
    payload = {
        "gem_id": "../traversal_test",
        "instruction": "test"
    }

    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422 # Unprocessable Entity (Validation Error)
    assert "string_pattern_mismatch" in str(response.json())

def test_setup_search_path_traversal_validation():
    payload = {
        "search_id": "../../traversal_search",
        "brief_notes": "test",
        "jd_content": "test"
    }

    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "string_pattern_mismatch" in str(response.json())

def test_run_pipeline_search_id_traversal_validation():
    payload = {
        "search_id": "../../traversal_run",
        "local_dir": "prompts",
        "model": "gemini-2.0-flash"
    }

    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_run_pipeline_local_dir_traversal_validation():
    # local_dir: pattern=r"^[a-zA-Z0-9_-][a-zA-Z0-9_/-]*$"
    # This pattern allows slashes but not leading slash or ..

    payload = {
        "search_id": "normal-search",
        "local_dir": "../traversal",
        "model": "gemini-2.0-flash"
    }

    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

    payload = {
        "search_id": "normal-search",
        "local_dir": "/abs/path",
        "model": "gemini-2.0-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_run_pipeline_valid_inputs():
    payload = {
        "search_id": "valid-search_123",
        "local_dir": "valid/path/dir-name",
        "model": "gemini-2.0-flash"
    }

    with patch("api.GEM6Orchestrator") as mock_orch, \
         patch("api.GeminiClient") as mock_gemini, \
         patch("api.load_local_inputs") as mock_load:

        mock_load.return_value = ({}, {})
        mock_instance = mock_orch.return_value
        mock_instance.run_pipeline = AsyncMock(return_value={})

        response = client.post("/api/v1/run", json=payload)

    assert response.status_code == 200
    if os.path.exists("runs/valid-search_123"):
        shutil.rmtree("runs/valid-search_123")
