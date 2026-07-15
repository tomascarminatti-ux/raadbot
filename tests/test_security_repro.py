import pytest
from fastapi.testclient import TestClient
from api import app
import os

client = TestClient(app, raise_server_exceptions=False)

def test_path_traversal_run():
    # search_id is used in os.path.join("runs", request.search_id, "outputs")
    response = client.post("/api/v1/run", json={
        "search_id": "../../vulnerable",
        "local_dir": "tests" # Just to pass validation
    })
    # Should now be 422 Unprocessable Entity
    assert response.status_code == 422

def test_path_traversal_setup():
    # search_id is used in os.path.join("runs", request.search_id, "outputs")
    response = client.post("/api/v1/search/setup", json={
        "search_id": "../../vulnerable_setup",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422

def test_path_traversal_refine():
    # gem_id is used in f"prompts/{request.gem_id}.md"
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../vulnerable_refine",
        "instruction": "test"
    })
    assert response.status_code == 422

def test_valid_id():
    # Test that valid IDs still work (at least pass validation)
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem1",
        "instruction": "test"
    })
    # Might be 500 if GEMINI_API_KEY is not set, but not 422
    assert response.status_code != 422
