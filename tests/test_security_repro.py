
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_refine_gem_path_traversal():
    # Attempt to access a file outside the prompts directory
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../README",
        "instruction": "test"
    })
    # After fix, it should return 422 Unprocessable Entity because of regex pattern
    assert response.status_code == 422


def test_run_pipeline_path_traversal():
    response = client.post("/api/v1/run", json={
        "search_id": "../../etc/passwd",
        "local_dir": "test"
    })
    # After fix, it should return 422 Unprocessable Entity
    assert response.status_code == 422


def test_run_pipeline_local_dir_traversal():
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id",
        "local_dir": "../outside"
    })
    # After fix, it should return 422 Unprocessable Entity
    assert response.status_code == 422
