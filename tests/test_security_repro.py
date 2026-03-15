import pytest
from fastapi.testclient import TestClient
from api import app
import os

client = TestClient(app)

def test_path_traversal_refine_gem():
    # Attempt to write to a file outside the prompts directory
    payload = {
        "gem_id": "../evil",
        "instruction": "make it evil"
    }

    response = client.post("/api/v1/gems/refine", json=payload)
    # Should be 422 because gem_id doesn't match the regex pattern
    assert response.status_code == 422

def test_path_traversal_run_pipeline_search_id():
    payload = {
        "search_id": "../evil_search",
        "local_dir": "data"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_path_traversal_run_pipeline_local_dir():
    payload = {
        "search_id": "valid_id",
        "local_dir": "../../etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "local_dir contains invalid characters" in response.json()["detail"][0]["msg"]

def test_absolute_path_run_pipeline_local_dir():
    payload = {
        "search_id": "valid_id",
        "local_dir": "/etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "local_dir contains invalid characters" in response.json()["detail"][0]["msg"]

def test_valid_payload():
    # This should pass validation even if it fails later due to missing files/API keys
    payload = {
        "search_id": "valid-123_ID",
        "local_dir": "runs/test"
    }
    response = client.post("/api/v1/run", json=payload)
    # It will probably return 400 because GEMINI_API_KEY is dummy or files not found,
    # but NOT 422.
    assert response.status_code != 422
