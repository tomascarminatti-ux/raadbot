import pytest
from fastapi.testclient import TestClient
from api import app
from unittest.mock import patch, mock_open
import config

client = TestClient(app)

def test_refine_gem_path_traversal():
    # Attempt to use path traversal in gem_id
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../config", "instruction": "make it better"}
    )
    # Should be rejected by Pydantic validation (422) because of pattern mismatch
    assert response.status_code == 422

def test_refine_gem_not_allowed():
    # Attempt to refine a gem not in the whitelist
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "gem6", "instruction": "make it better"}
    )
    # Should be rejected by whitelist check (403)
    assert response.status_code == 403

def test_run_pipeline_path_traversal():
    response = client.post(
        "/api/v1/run",
        json={"search_id": "../evil", "local_dir": "test_inputs"}
    )
    # Should be rejected by Pydantic validation (422)
    assert response.status_code == 422

def test_setup_search_path_traversal():
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../evil",
            "brief_notes": "notes",
            "jd_content": "jd"
        }
    )
    # Should be rejected by Pydantic validation (422)
    assert response.status_code == 422

@patch("agent.gemini_client.GeminiClient.run_gem")
def test_valid_ids_accepted_validation(mock_run_gem):
    """Verify that valid IDs pass the Pydantic validation."""
    mock_run_gem.return_value = {"markdown": "new prompt", "data": {}}

    # Mock open to prevent actually writing to the file system during tests
    with patch("builtins.open", mock_open(read_data="current prompt")):
        with patch("os.path.exists", return_value=True):
            response = client.post(
                "/api/v1/gems/refine",
                json={"gem_id": "gem1", "instruction": "make it better"}
            )
            # It should pass Pydantic validation and proceed
            assert response.status_code != 422
