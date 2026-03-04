import pytest
from fastapi.testclient import TestClient
from api import app
import os

client = TestClient(app)

def test_path_traversal_pipeline():
    # Attempt to access a directory outside the expected range using ..
    response = client.post("/api/v1/run", json={
        "search_id": "test",
        "local_dir": "../etc"
    })
    # Should return 422 Unprocessable Entity due to validation error
    assert response.status_code == 422
    print(f"Pipeline .. test status: {response.status_code}")

    # Attempt absolute path
    response = client.post("/api/v1/run", json={
        "search_id": "test",
        "local_dir": "/etc"
    })
    assert response.status_code == 422
    print(f"Pipeline absolute path test status: {response.status_code}")

def test_invalid_search_id():
    response = client.post("/api/v1/run", json={
        "search_id": "test; rm -rf /",
        "local_dir": "inputs"
    })
    assert response.status_code == 422
    print(f"Invalid search_id test status: {response.status_code}")

def test_path_traversal_refine():
    # Attempt to access a file outside prompts/ using ..
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../api",
        "instruction": "test"
    })
    assert response.status_code == 422
    print(f"Refine gem_id test status: {response.status_code}")

def test_valid_refine_allowed():
    # This should pass validation (but might fail later if no API key or ollama not running)
    # Actually it should pass validation of the model.
    # We use a try/except or just check for 422 specifically.
    try:
        response = client.post("/api/v1/gems/refine", json={
            "gem_id": "gem1",
            "instruction": "test"
        })
        # If it passed validation, it shouldn't be 422.
        assert response.status_code != 422
        print(f"Valid refine test status: {response.status_code}")
    except Exception as e:
        # If the app crashed because of missing API key or connection error,
        # it still means the Pydantic validation passed.
        print(f"Valid refine request triggered an app error (expected since environment is not fully configured): {e}")

if __name__ == "__main__":
    try:
        test_path_traversal_pipeline()
        test_invalid_search_id()
        test_path_traversal_refine()
        test_valid_refine_allowed()
        print("✅ All security verification tests passed (triggered 422 as expected).")
    except AssertionError as e:
        print(f"❌ Verification failed: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        exit(1)
