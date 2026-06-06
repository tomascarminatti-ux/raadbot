import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, mock_open
from api import app
import config
import os

client = TestClient(app)

def test_refine_gem_path_traversal():
    # Attempt to read/write outside of the prompts directory
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../config", "instruction": "test"}
    )
    # Now returns 422 because of pattern validation
    assert response.status_code == 422

def test_run_pipeline_path_traversal():
    response = client.post(
        "/api/v1/run",
        json={"search_id": "../../traversal_test", "local_dir": "tests"}
    )
    # Now returns 422 because of pattern validation
    assert response.status_code == 422

@patch("api.os.path.exists")
@patch("api.open", new_callable=mock_open, read_data="original prompt")
@patch("agent.gemini_client.GeminiClient.run_gem")
def test_refine_gem_whitelist_valid(mock_run_gem, mock_file, mock_exists):
    # gem1 is in whitelist
    mock_exists.return_value = True
    mock_run_gem.return_value = {"markdown": "refined prompt", "data": {}}

    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "gem1", "instruction": "test"}
    )
    assert response.status_code == 200
    # Verify it tried to read/write the correct file
    mock_file.assert_any_call("prompts/gem1.md", "r", encoding="utf-8")
    mock_file.assert_any_call("prompts/gem1.md", "w", encoding="utf-8")

def test_refine_gem_whitelist_invalid():
    # "secret_gem" is not in whitelist but matches pattern
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "secret_gem", "instruction": "test"}
    )
    assert response.status_code == 403
