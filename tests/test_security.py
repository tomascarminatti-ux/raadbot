import os
import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_run():
    # Attempt to use a malicious search_id
    # Pydantic should catch this and return 422
    payload = {
        "search_id": "../../malicious",
        "local_dir": "tests/test_data"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text

def test_path_traversal_refine():
    # Attempt to use a malicious gem_id
    payload = {
        "gem_id": "../api",
        "instruction": "Add a malicious comment"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "gem_id" in response.text

from unittest.mock import patch, MagicMock

def test_safe_ids_pass_validation():
    # Valid IDs should pass the Pydantic validation layer
    payload = {
        "search_id": "valid-search-123",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    # Mock GeminiClient to avoid network calls during this test
    with patch("api.GeminiClient") as mock_gemini:
        mock_instance = mock_gemini.return_value
        mock_instance.run_gem.return_value = {"data": {}, "markdown": ""}

        response = client.post("/api/v1/search/setup", json=payload)
        # Should NOT be a 422 validation error
        assert response.status_code != 422

def test_local_dir_validation():
    # Valid local_dir should pass
    payload = {
        "search_id": "valid-search",
        "local_dir": "path/to/data"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code != 422

    # Malicious local_dir should fail
    payload["local_dir"] = "/absolute/path"
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

    payload["local_dir"] = "../traversal"
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
