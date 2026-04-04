import os
# Set environment variable before importing api
os.environ["GEMINI_API_KEY"] = "dummy"

import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_search_id():
    # Attempt to use path traversal in search_id
    payload = {
        "search_id": "../traversal_test",
        "local_dir": "tests"
    }
    response = client.post("/api/v1/run", json=payload)
    # After the fix, we expect 422 Unprocessable Entity due to Pydantic validation
    assert response.status_code == 422
    assert not os.path.exists("traversal_test")
    assert not os.path.exists("runs/../traversal_test")

def test_path_traversal_local_dir():
    # Absolute path should fail regex
    payload = {
        "search_id": "valid_id",
        "local_dir": "/etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

    # Traversal should fail regex
    payload = {
        "search_id": "valid_id",
        "local_dir": "etc/../../traversal"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_path_traversal_gem_id():
    payload = {
        "gem_id": "../api",
        "instruction": "make it better"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
