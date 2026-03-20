from fastapi.testclient import TestClient
import os
import pytest
from api import app

client = TestClient(app)

def test_path_traversal_refine_gem_v2():
    # Attempt to access a file outside the prompts directory
    # Now it should fail with 422 because of Pydantic validation regex
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../config",
        "instruction": "test"
    })
    assert response.status_code == 422

def test_path_traversal_setup_search_v2():
    # search_id is used to create a directory
    # Now it should fail with 422 because of Pydantic validation regex
    response = client.post("/api/v1/search/setup", json={
        "search_id": "../../vulnerable_dir",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422
    assert not os.path.exists("vulnerable_dir")

def test_valid_payload_validation():
    # Test with valid payload to ensure validation passes
    # We use a non-existent gem_id but with valid format to see if it passes validation
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "valid_gem_id",
        "instruction": "test"
    })
    # Validation should pass (not 422), but it should be 404 because valid_gem_id.md doesn't exist
    assert response.status_code == 404
