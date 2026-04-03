import pytest
from fastapi.testclient import TestClient
import os
import shutil

# Set dummy key for testing
os.environ["GEMINI_API_KEY"] = "dummy"

from api import app

client = TestClient(app)

def test_path_traversal_validation():
    # Test search_id validation
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../evil_dir",
            "local_dir": "tests"
        }
    )
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

    # Test gem_id validation
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "invalid/path",
            "instruction": "test"
        }
    )
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

def test_local_dir_validation():
    # Test local_dir starting with slash (not allowed by regex)
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "/etc/passwd"
        }
    )
    assert response.status_code == 422

    # Test local_dir with traversal (blocked by validator)
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "some/../path"
        }
    )
    assert response.status_code == 422
    assert "parent directory references" in response.text

def test_local_dir_with_dots():
    # Test local_dir with dots (should pass validation)
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "data_v1.0/inputs"
        }
    )
    # It should not be 422 (validation error)
    assert response.status_code != 422
