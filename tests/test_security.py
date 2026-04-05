import pytest
from fastapi.testclient import TestClient
import os

# Set dummy API key before importing api to bypass startup check
os.environ["GEMINI_API_KEY"] = "dummy"

from api import app

client = TestClient(app)

def test_path_traversal_local_dir():
    # Attempting to read a file outside the intended directory via local_dir
    payload = {
        "search_id": "test_traversal",
        "local_dir": "../../etc",
        "model": "gemini-2.0-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    # Pydantic validation failure returns 422
    assert response.status_code == 422
    print("test_path_traversal_local_dir passed with 422")

def test_path_traversal_search_id():
    # search_id with traversal characters
    payload = {
        "search_id": "../../../tmp/evil",
        "local_dir": "tests",
        "model": "gemini-2.0-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    print("test_path_traversal_search_id passed with 422")

def test_valid_payload():
    payload = {
        "search_id": "valid-id_123",
        "local_dir": "tests",
        "model": "gemini-2.0-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    # Should get past validation. Might fail later because of missing files, but not 422.
    assert response.status_code != 422
    print("test_valid_payload passed validation")

if __name__ == "__main__":
    test_path_traversal_local_dir()
    test_path_traversal_search_id()
    test_valid_payload()
