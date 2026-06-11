import pytest
from fastapi.testclient import TestClient
from api import app
import config
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_identifier_validation_path_traversal():
    """Verify that identifiers like search_id block path traversal sequences."""
    # Attempt path traversal via search_id in /api/v1/run
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../root_file",
            "local_dir": "tests/data"
        }
    )
    # Pydantic validation should fail
    assert response.status_code == 422
    assert "search_id" in response.text

def test_gem_id_whitelist():
    """Verify that only allowed GEM IDs can be refined."""
    # Allowed gem
    with patch("api.GeminiClient") as mock_gemini:
        mock_instance = mock_gemini.return_value
        mock_instance.run_gem.return_value = {"markdown": "new prompt", "data": {}}

        response = client.post(
            "/api/v1/gems/refine",
            json={
                "gem_id": "gem1",
                "instruction": "test"
            }
        )
        assert response.status_code == 200

    # Disallowed gem
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "secret_file",
            "instruction": "test"
        }
    )
    assert response.status_code == 403
    assert "Gem ID not allowed" in response.json()["detail"]

    # Path traversal attempt in gem_id
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "../../etc/passwd",
            "instruction": "test"
        }
    )
    # Should fail pydantic validation first if pattern blocks dots/slashes
    assert response.status_code == 422

def test_secure_error_messages():
    """Verify that trigger_pipeline returns generic error messages."""
    with patch("api.run_pipeline", side_effect=Exception("Database connection failed: user=admin pass=123")):
        response = client.post(
            "/api/v1/run",
            json={
                "search_id": "test_search",
                "local_dir": "tests/data"
            }
        )
        assert response.status_code == 500
        assert "Internal server error during pipeline execution" in response.json()["detail"]
        assert "Database connection failed" not in response.json()["detail"]
        assert "admin" not in response.json()["detail"]
