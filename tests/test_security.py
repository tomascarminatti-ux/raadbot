import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_search_id():
    # Test path traversal in search_id for /api/v1/run
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../../evil",
            "local_dir": "test_data"
        }
    )
    # If not validated, it might return 400 or 500 depending on file existence,
    # but we want it to be 422 (Unprocessable Entity) due to Pydantic validation.
    assert response.status_code == 422

def test_path_traversal_gem_id():
    # Test path traversal in gem_id for /api/v1/gems/refine
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "../../secret",
            "instruction": "make it better"
        }
    )
    assert response.status_code == 422

def test_path_traversal_local_dir():
    # Test path traversal in local_dir for /api/v1/run
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "/etc"
        }
    )
    assert response.status_code == 422
