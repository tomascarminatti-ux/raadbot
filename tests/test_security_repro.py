import os
import json
import pytest
from fastapi.testclient import TestClient

# Mock GEMINI_API_KEY before importing app
os.environ["GEMINI_API_KEY"] = "dummy-key"
import config
config.GEMINI_API_KEY = "dummy-key"

from api import app

client = TestClient(app)

def test_path_traversal_search_id():
    payload = {
        "search_id": "../evil_dir",
        "local_dir": "tests",
        "model": "gemini-1.5-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    print(f"Search ID Traversal Response: {response.status_code}")
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    assert "string_pattern_mismatch" in str(response.json())

def test_path_traversal_local_dir():
    payload = {
        "search_id": "valid_id",
        "local_dir": "/etc",
        "model": "gemini-1.5-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    print(f"Local Dir Absolute Response: {response.status_code}")
    assert response.status_code == 422, f"Expected 422 for absolute path, got {response.status_code}"
    # When Pydantic validator fails, it returns a 422 with a specific detail
    assert "Value error" in str(response.json())

    payload = {
        "search_id": "valid_id",
        "local_dir": "some/../path",
        "model": "gemini-1.5-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    print(f"Local Dir Traversal Response: {response.status_code}")
    assert response.status_code == 422, f"Expected 422 for traversal path, got {response.status_code}"
    assert "Value error" in str(response.json())

def test_path_traversal_refine_gem():
    payload = {
        "gem_id": "../evil_prompt",
        "instruction": "Make it better"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    print(f"Refine GEM ID Traversal Response: {response.status_code}")
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    assert "string_pattern_mismatch" in str(response.json())

if __name__ == "__main__":
    try:
        test_path_traversal_search_id()
        test_path_traversal_local_dir()
        test_path_traversal_refine_gem()
        print("ALL SECURITY TESTS PASSED")
    except AssertionError as e:
        print(f"SECURITY TEST FAILED: {e}")
        print(f"JSON response was: {json.dumps(response.json() if 'response' in locals() else {}, indent=2)}")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
