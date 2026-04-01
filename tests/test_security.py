import pytest
from fastapi.testclient import TestClient
import os
import sys
import shutil
from unittest.mock import MagicMock, patch

# Set dummy API key to bypass startup check
os.environ["GEMINI_API_KEY"] = "dummy"

import api
from api import app

client = TestClient(app)

def test_path_traversal_setup_search_blocked_by_validation():
    # search_id with ".." should be blocked by Pydantic validation (422 Unprocessable Entity)
    search_id = "../vulnerable_dir"
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": search_id,
            "brief_notes": "test",
            "jd_content": "test"
        }
    )
    assert response.status_code == 422
    assert "string_pattern_mismatch" in str(response.json())

def test_path_traversal_refine_gem_blocked_by_validation():
    # gem_id with ".." should be blocked by Pydantic validation (422 Unprocessable Entity)
    gem_id = "../config"
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": gem_id, "instruction": "test"}
    )
    assert response.status_code == 422
    assert "string_pattern_mismatch" in str(response.json())

def test_ssrf_webhook_url_blocked():
    # Localhost/Private IP in webhook_url should be blocked by validator (422)

    payload = {
        "search_id": "test_search",
        "local_dir": "test_dir",
        "webhook_url": "http://localhost:8000/callback"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Localhost webhook URLs are not allowed" in str(response.json())

    payload["webhook_url"] = "http://192.168.1.1/callback"
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Private or reserved IP addresses are not allowed" in str(response.json())

def test_path_traversal_local_dir_blocked():
    # local_dir with ".." should be blocked
    payload = {
        "search_id": "test_search",
        "local_dir": "../../etc",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "string_pattern_mismatch" in str(response.json())

def test_valid_requests_pass_validation():
    # A valid search_id and local_dir should pass validation
    with patch('api.run_pipeline') as mock_run:
        mock_run.return_value = {"status": "success"}
        payload = {
            "search_id": "valid-search_123",
            "local_dir": "data/inputs",
        }
        response = client.post("/api/v1/run", json=payload)
        # Check for 200 or any non-422 status that means it passed validation
        assert response.status_code != 422
