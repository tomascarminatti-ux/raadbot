import os
import pytest
from fastapi.testclient import TestClient
from api import app
import config
from unittest.mock import patch

client = TestClient(app)

def test_path_traversal_refine_gem_validation():
    # Attempt to bypass using path traversal characters
    payload = {
        "gem_id": "../danger",
        "instruction": "REPLACE EVERYTHING"
    }
    response = client.post("/api/v1/gems/refine", json=payload)

    # Should be 422 Unprocessable Entity because of ID_PATTERN regex
    assert response.status_code == 422
    assert "pattern" in str(response.json())

def test_whitelist_refine_gem():
    # Attempt to access a valid file but not in whitelist (if we had any)
    # Actually, all gems in GEM_CONFIGS are whitelisted.
    # Let's try one that matches regex but NOT in ALLOWED_GEMS
    payload = {
        "gem_id": "gem99",
        "instruction": "REPLACE EVERYTHING"
    }
    response = client.post("/api/v1/gems/refine", json=payload)

    # Should be 403 Forbidden because it's not in ALLOWED_GEMS
    assert response.status_code == 403
    assert response.json()["detail"] == "GEM access restricted"

def test_path_traversal_run_pipeline():
    payload = {
        "search_id": "../../../tmp/pwned",
        "local_dir": "tests"
    }
    response = client.post("/api/v1/run", json=payload)

    assert response.status_code == 422
    assert not os.path.exists("/tmp/pwned")

def test_legitimate_request_format():
    # Test that valid IDs still work (this won't actually run the pipeline
    # because of missing API keys/files, but should pass Pydantic validation)
    payload = {
        "gem_id": "gem1",
        "instruction": "Make it better"
    }
    # Mock GeminiClient.run_gem to avoid calling external services
    with patch("agent.gemini_client.GeminiClient.run_gem") as mock_run:
        mock_run.return_value = {"markdown": "Refined prompt", "raw": "Refined prompt"}
        response = client.post("/api/v1/gems/refine", json=payload)

        # It might fail with 404 if the prompt file doesn't exist, but it shouldn't be 422
        assert response.status_code != 422

if __name__ == "__main__":
    pytest.main([__file__])
