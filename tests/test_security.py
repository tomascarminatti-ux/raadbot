import pytest
from fastapi.testclient import TestClient
from api import app
import os
from unittest.mock import patch, MagicMock

client = TestClient(app)

@patch("agent.gemini_client.GeminiClient.run_gem")
def test_path_traversal_search_id(mock_run_gem):
    mock_run_gem.return_value = {"data": {}, "markdown": ""}
    # Attempt to use path traversal in search_id
    response = client.post("/api/v1/search/setup", json={
        "search_id": "../traversal_test",
        "brief_notes": "test",
        "jd_content": "test"
    })
    # We want it to be blocked (e.g. 422 or 400).
    assert response.status_code in [422, 400]
    # Check that the folder was NOT created outside 'runs'
    assert not os.path.exists("../traversal_test")
    assert not os.path.exists("traversal_test")

def test_path_traversal_refine_gem():
    # Attempt to use path traversal in gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../../api",
        "instruction": "make it secure"
    })
    # Should be blocked
    assert response.status_code in [422, 404, 400]

def test_path_traversal_local_dir():
    # local_dir should not be an absolute path or contain ..
    response = client.post("/api/v1/run", json={
        "search_id": "test_run",
        "local_dir": "/etc"
    })
    assert response.status_code in [422, 400]

    response = client.post("/api/v1/run", json={
        "search_id": "test_run",
        "local_dir": "../secrets"
    })
    assert response.status_code in [422, 400]
