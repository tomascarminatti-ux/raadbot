import os
import pytest
from fastapi.testclient import TestClient

# Mock GEMINI_API_KEY for testing
os.environ["GEMINI_API_KEY"] = "dummy_key"

from api import app

client = TestClient(app)

def test_fixed_path_traversal_search_id():
    """Verify that search_id now triggers 422 for path traversal."""
    response = client.post("/api/v1/run", json={
        "search_id": "../traversal_test",
        "local_dir": "runs/SEARCH-TEST-001/inputs"
    })
    print(f"Status: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 422
    assert "search_id" in str(response.json())

def test_fixed_path_traversal_local_dir_absolute():
    """Verify that local_dir triggers 422 for absolute paths."""
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "/etc"
    })
    print(f"Status: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 422
    assert "local_dir" in str(response.json())

def test_fixed_path_traversal_local_dir_traversal():
    """Verify that local_dir triggers 422 for path traversal."""
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "runs/../../etc"
    })
    print(f"Status: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 422
    assert "local_dir" in str(response.json())

def test_fixed_path_traversal_gem_id():
    """Verify that gem_id triggers 422 for path traversal."""
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../config",
        "instruction": "test"
    })
    print(f"Status: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 422
    assert "gem_id" in str(response.json())

def test_valid_request():
    """Verify that valid requests still work."""
    response = client.post("/api/v1/run", json={
        "search_id": "valid_search_123",
        "local_dir": "runs/SEARCH-TEST-001/inputs"
    })
    # Should not be 422. Might be 400 because inputs might not be found in some environments,
    # but the validation should pass.
    print(f"Status: {response.status_code}, Body: {response.json()}")
    assert response.status_code != 422
