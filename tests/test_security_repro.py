from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_refine_gem():
    # Attempt to access a file outside the prompts directory
    # Even if it doesn't exist, we want to see if the API allows the path construction
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../config", "instruction": "test"}
    )
    # If vulnerable, it might return 404 (file not found) or 500
    # If protected, it should return 422 Unprocessable Entity due to validation error
    assert response.status_code == 422

def test_path_traversal_trigger_pipeline():
    response = client.post(
        "/api/v1/run",
        json={"search_id": "../../etc/passwd", "local_dir": "."}
    )
    assert response.status_code == 422

def test_path_traversal_setup_search():
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "test/../traversal",
            "brief_notes": "notes",
            "jd_content": "jd"
        }
    )
    assert response.status_code == 422
