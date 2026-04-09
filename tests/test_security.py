import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# Set dummy API key for import time if needed, although api.py doesn't require it at import
os.environ["GEMINI_API_KEY"] = "test_key"

from api import app

client = TestClient(app)

def test_pipeline_run_path_traversal_local_dir():
    # Attempting to use path traversal in local_dir
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "test_search",
            "local_dir": "../../etc",
            "model": "gemini-2.0-flash"
        }
    )
    # If validation is missing, it might return 400 (if run_pipeline fails later)
    # or even try to process it.
    # We want it to be 422 Unprocessable Entity because of Pydantic validation.
    assert response.status_code == 422

def test_pipeline_run_path_traversal_search_id():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../hacked",
            "local_dir": "data/inputs",
            "model": "gemini-2.0-flash"
        }
    )
    assert response.status_code == 422

def test_setup_search_path_traversal_search_id():
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "/absolute/path",
            "brief_notes": "notes",
            "jd_content": "jd"
        }
    )
    assert response.status_code == 422

def test_refine_gem_path_traversal_gem_id():
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "../config.py",
            "instruction": "overwrite"
        }
    )
    assert response.status_code == 422

def test_refine_gem_invalid_gem_id():
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "gem99",
            "instruction": "refine"
        }
    )
    assert response.status_code == 422
