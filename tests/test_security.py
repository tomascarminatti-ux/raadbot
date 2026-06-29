import pytest
from fastapi.testclient import TestClient
from api import app
import os
import shutil

client = TestClient(app)

def test_path_traversal_run_pipeline():
    # Attempt to use a path traversal search_id
    evil_id = "../evil_dir"
    response = client.post("/api/v1/run", json={
        "search_id": evil_id,
        "local_dir": "prompts"
    })
    # Should be 422 Unprocessable Entity due to regex validation
    assert response.status_code == 422
    assert not os.path.exists("evil_dir")

def test_path_traversal_setup_search():
    evil_id = "../evil_setup"
    response = client.post("/api/v1/search/setup", json={
        "search_id": evil_id,
        "brief_notes": "test",
        "jd_content": "test"
    })
    # Should be 422
    assert response.status_code == 422
    assert not os.path.exists("evil_setup")

def test_path_traversal_refine_gem():
    evil_gem_id = "../evil_gem"
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": evil_gem_id,
        "instruction": "test"
    })
    # Should be 422
    assert response.status_code == 422

def test_valid_ids():
    # Verify that valid IDs still work (or at least pass validation)
    # We mock GeminiClient to avoid external calls and errors
    from unittest.mock import patch
    with patch("agent.gemini_client.GeminiClient.run_gem") as mock_run:
        mock_run.return_value = {"markdown": "test", "data": {}}
        response = client.post("/api/v1/search/setup", json={
            "search_id": "valid-id_123",
            "brief_notes": "test",
            "jd_content": "test"
        })
        # If it passes validation, it might still fail later due to missing keys/etc,
        # but here we just want to see it didn't get a 422.
        assert response.status_code != 422

if __name__ == "__main__":
    pytest.main([__file__])
