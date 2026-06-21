import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api import app
import config

client = TestClient(app)

def test_path_traversal_refine_gem():
    # Attempt path traversal via gem_id - should fail pydantic validation (422)
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../README", "instruction": "test"}
    )
    assert response.status_code == 422

def test_whitelist_refine_gem():
    # Non-whitelisted but valid pattern gem_id - should return 403 Forbidden
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "gem99", "instruction": "test"}
    )
    assert response.status_code == 403

def test_path_traversal_setup_search():
    # Attempt path traversal via search_id - should fail pydantic validation (422)
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../../vulnerable",
            "brief_notes": "test",
            "jd_content": "test"
        }
    )
    assert response.status_code == 422

def test_valid_setup_search_pydantic():
    # Valid identifier should pass pydantic validation
    with patch("api.GeminiClient") as mock_gemini:
        mock_instance = mock_gemini.return_value
        mock_instance.run_gem.return_value = {"data": {"mandate_summary": "ok"}, "markdown": "ok"}

        response = client.post(
            "/api/v1/search/setup",
            json={
                "search_id": "valid_search-123",
                "brief_notes": "test",
                "jd_content": "test"
            }
        )
        # Should succeed now that LLM is mocked
        assert response.status_code == 200
