from fastapi.testclient import TestClient
from api import app
import pytest
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_path_traversal_gem_id():
    # Attempt to use path traversal in gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../../README",
        "instruction": "test"
    })
    # Pydantic validation error should return 422
    assert response.status_code == 422

def test_non_whitelisted_gem_id():
    # Attempt to use a non-whitelisted gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem7",
        "instruction": "test"
    })
    # Whitelist check should return 403
    assert response.status_code == 403

def test_path_traversal_search_id():
    # Attempt to use path traversal in search_id
    response = client.post("/api/v1/run", json={
        "search_id": "../run_traversal",
        "local_dir": "./"
    })
    # Pydantic validation error should return 422
    assert response.status_code == 422

@patch("api.GeminiClient")
def test_valid_gem_id_pass_validation(mock_gemini_class):
    # Mock GeminiClient.run_gem to return a successful result
    mock_instance = mock_gemini_class.return_value
    mock_instance.run_gem.return_value = {"markdown": "Refined prompt", "data": {}}

    # Valid GEM ID should pass validation
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem1",
        "instruction": "test"
    })
    # Should be 200 since we mocked the client
    assert response.status_code == 200
