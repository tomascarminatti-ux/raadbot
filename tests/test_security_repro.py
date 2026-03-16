from fastapi.testclient import TestClient
from api import app
import pytest

client = TestClient(app)

def test_path_traversal_search_id():
    # Attempt to use a search_id with path traversal
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../evil",
            "local_dir": "test_data"
        }
    )
    # With Pydantic validation, this should return 422 Unprocessable Entity
    assert response.status_code == 422

def test_path_traversal_local_dir():
    # Attempt to use a local_dir with path traversal
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "local_dir": "../../etc/passwd"
        }
    )
    assert response.status_code == 422

def test_absolute_path_local_dir():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "local_dir": "/etc/passwd"
        }
    )
    assert response.status_code == 422

def test_path_traversal_gem_id():
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "../../etc/passwd",
            "instruction": "ignore"
        }
    )
    assert response.status_code == 422

def test_valid_payload():
    # This should pass validation (it might still fail downstream if dummy key is used,
    # but we care about validation here)
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_search-123",
            "local_dir": "data/inputs"
        }
    )
    # It shouldn't be 422. It might be 400 (if no drive_folder/local_dir found) or 500
    assert response.status_code != 422
