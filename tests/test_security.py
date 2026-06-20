import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_refine_gem_path_traversal():
    """Verify that path traversal in gem_id is blocked by validation."""
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../README", "instruction": "hacked"}
    )
    # Expect 422 Unprocessable Entity due to Pydantic pattern validation
    assert response.status_code == 422

def test_refine_gem_non_whitelisted():
    """Verify that non-whitelisted GEM IDs are rejected."""
    # This matches the ID_PATTERN but should fail whitelisting
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "gem99", "instruction": "hacked"}
    )
    # Once implemented, this should return 403 Forbidden
    assert response.status_code == 403

def test_pipeline_run_path_traversal():
    """Verify that path traversal in search_id is blocked by validation."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../../etc/passwd",
            "local_dir": "runs/test"
        }
    )
    assert response.status_code == 422

def test_search_setup_path_traversal():
    """Verify that path traversal in search_id is blocked by validation."""
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "invalid/path",
            "brief_notes": "test",
            "jd_content": "test"
        }
    )
    assert response.status_code == 422
