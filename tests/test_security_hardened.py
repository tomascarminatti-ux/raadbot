import pytest
from fastapi.testclient import TestClient
from api import app
import os

client = TestClient(app)

def test_refine_gem_path_traversal():
    # Attempt to access a file outside prompts/ using path traversal
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../target", "instruction": "make it better"}
    )
    # It should return 422 Unprocessable Entity because of pattern mismatch
    assert response.status_code == 422

def test_refine_gem_whitelist():
    # Attempt to access a valid path but not in whitelist
    # ID_PATTERN allows 'secret', but ALLOWED_GEMS does not.
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "secret", "instruction": "make it better"}
    )
    # It should return 403 Forbidden because it's not in ALLOWED_GEMS
    assert response.status_code == 403

from unittest.mock import patch

def test_refine_gem_valid_id():
    # Valid ID and in whitelist.
    # Mocking run_gem to avoid connection errors.
    # Also mocking 'open' to avoid overwriting the actual prompt file during tests.
    with patch("agent.gemini_client.GeminiClient.run_gem") as mock_run:
        mock_run.return_value = {"markdown": "new prompt", "json": {}}
        with patch("api.open", create=True) as mock_open:
            response = client.post(
                "/api/v1/gems/refine",
                json={"gem_id": "gem1", "instruction": "make it better"}
            )
            assert response.status_code == 200
            assert response.json()["status"] == "success"

def test_refine_gem_invalid_pattern():
    # Invalid pattern (e.g. including dots)
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "gem.1", "instruction": "make it better"}
    )
    assert response.status_code == 422

def test_id_validation_path_traversal_setup_search():
    # search_id is used in os.path.join("runs", request.search_id, "outputs")
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../../evil",
            "brief_notes": "notes",
            "jd_content": "jd"
        }
    )
    # It should return 422 Unprocessable Entity
    assert response.status_code == 422
