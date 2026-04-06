import os
import pytest
from fastapi.testclient import TestClient

# Mock GEMINI_API_KEY for testing
os.environ["GEMINI_API_KEY"] = "dummy"

from api import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_gemini():
    with patch("api.GeminiClient") as mock:
        mock_instance = MagicMock()
        mock_instance.run_gem.return_value = {"data": {}, "markdown": "mocked"}
        mock.return_value = mock_instance
        yield mock

@pytest.fixture(autouse=True)
def mock_orchestrator():
    with patch("api.GEM6Orchestrator") as mock:
        mock_instance = MagicMock()
        mock_instance.run_pipeline.return_value = asyncio.Future()
        mock_instance.run_pipeline.return_value.set_result(None)
        mock.return_value = mock_instance
        yield mock

import asyncio

def test_search_id_traversal():
    print("Testing search_id traversal...")
    payload = {
        "search_id": "../../evil",
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

def test_local_dir_traversal_absolute():
    print("Testing local_dir traversal (absolute path)...")
    payload = {
        "search_id": "valid_id",
        "local_dir": "/etc/passwd",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

def test_local_dir_traversal_dot_dot():
    print("Testing local_dir traversal (dot-dot)...")
    payload = {
        "search_id": "valid_id",
        "local_dir": "runs/../../etc/passwd",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    # In this case it can be value_error from our validator or pattern mismatch
    assert response.status_code == 422

def test_local_dir_valid_with_dots():
    print("Testing local_dir with dots in middle...")
    payload = {
        "search_id": "valid_id",
        "local_dir": "folder/v1.0/data.txt",
    }
    response = client.post("/api/v1/run", json=payload)
    # Should NOT be 422. Might be 400 if it proceeds to run_pipeline and fails to find file.
    assert response.status_code != 422

def test_gem_id_traversal():
    print("Testing gem_id traversal...")
    payload = {
        "gem_id": "../etc/passwd",
        "instruction": "test"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

def test_valid_ids():
    print("Testing valid identifiers...")
    payload = {
        "search_id": "search-123_ABC",
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    # Should NOT be 422
    assert response.status_code != 422
