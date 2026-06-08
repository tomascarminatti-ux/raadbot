import pytest
from fastapi.testclient import TestClient
from api import app
import config
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_pipeline_run_valid_id():
    # Valid ID should pass Pydantic validation (but might fail later due to missing keys/dirs)
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id_123",
        "local_dir": "nonexistent"
    })
    # We expect 400 because GEMINI_API_KEY might be missing or dir nonexistent,
    # but not 422 (Unprocessable Entity) which is Pydantic validation error.
    assert response.status_code != 422

def test_pipeline_run_invalid_id():
    # Invalid characters in search_id
    response = client.post("/api/v1/run", json={
        "search_id": "invalid;id",
        "local_dir": "nonexistent"
    })
    assert response.status_code == 422
    assert "pattern" in response.text.lower()

def test_refine_gem_path_traversal():
    # Attempt path traversal
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../config",
        "instruction": "steal secrets"
    })
    # blocked by regex pattern or whitelist
    assert response.status_code in [422, 403]

def test_refine_gem_not_in_whitelist():
    # Valid characters but not in whitelist
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "secret_file",
        "instruction": "overwrite"
    })
    assert response.status_code == 403
    assert "restricted" in response.json()["detail"]

def test_refine_gem_valid_whitelist():
    # This should pass Pydantic and whitelist
    # Mock GeminiClient to avoid connection errors
    with patch("api.GeminiClient") as mock_gemini_class:
        mock_instance = mock_gemini_class.return_value
        mock_instance.run_gem.return_value = {"markdown": "Optimized prompt", "json": {}}

        response = client.post("/api/v1/gems/refine", json={
            "gem_id": "gem1",
            "instruction": "make it better"
        })
        # Should not be 403 or 422
        assert response.status_code not in [403, 422]

def test_setup_search_invalid_id():
    response = client.post("/api/v1/search/setup", json={
        "search_id": "hacker/space",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422
