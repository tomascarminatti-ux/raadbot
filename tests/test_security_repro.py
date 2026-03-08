from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_search_id_traversal_run():
    # Attempt to use path traversal in search_id for /api/v1/run
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../../dangerous",
            "local_dir": "tests",  # Just to avoid other errors
        },
    )
    # If it works, it might create a directory outside 'runs'
    assert response.status_code == 422 or ".." not in response.json().get("detail", "")


def test_search_id_traversal_setup():
    # Attempt to use path traversal in search_id for /api/v1/search/setup
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../../dangerous_setup",
            "brief_notes": "test",
            "jd_content": "test",
        },
    )
    # We expect this to fail with 422 if we add validation
    assert response.status_code == 422


def test_gem_id_traversal_refine():
    # Attempt to use path traversal in gem_id for /api/v1/gems/refine
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "../api",  # trying to overwrite api.py maybe?
            "instruction": "test",
        },
    )
    # We expect this to fail with 422 if we add validation
    assert response.status_code == 422


def test_local_dir_traversal():
    # Attempt to use path traversal in local_dir for /api/v1/run
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "test_search",
            "local_dir": "/etc",  # trying to access absolute path
        },
    )
    assert response.status_code == 422
