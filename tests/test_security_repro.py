import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_refine_gem_path_traversal():
    # Attempt to access a file outside the prompts directory
    # Even if it appends .md, we can try to see if it accepts the path
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../config", "instruction": "test"}
    )
    # If it's not protected, it might try to open prompts/../config.md
    # We want this to be rejected with 422 (Unprocessable Entity) or at least not 404/500 if we implement validation
    assert response.status_code == 422 or response.status_code == 400

def test_run_pipeline_path_traversal():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "test_search",
            "local_dir": "/etc"
        }
    )
    # Should be rejected if we have proper validation
    assert response.status_code == 422 or response.status_code == 400

def test_setup_search_path_traversal():
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../../vulnerable",
            "brief_notes": "notes",
            "jd_content": "jd"
        }
    )
    # Should be rejected
    assert response.status_code == 422 or response.status_code == 400
