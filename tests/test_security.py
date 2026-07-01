from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_path_traversal_search_id():
    # Attempting path traversal via search_id
    payload = {
        "search_id": "../evil",
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    # If validation is working, it should return 422 Unprocessable Entity
    assert response.status_code == 422


def test_path_traversal_local_dir():
    # Attempting path traversal via local_dir
    payload = {
        "search_id": "valid-id",
        "local_dir": "/etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422


def test_invalid_gem_id():
    payload = {
        "gem_id": "invalid/path",
        "instruction": "refine"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
