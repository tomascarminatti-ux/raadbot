import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_api_v1_run():
    """Test that path traversal in search_id is blocked by Pydantic validation."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../../etc/passwd",
            "local_dir": "tests"
        }
    )
    # Pydantic validation error should return 422
    assert response.status_code == 422

def test_path_traversal_api_v1_search_setup():
    """Test that path traversal in search_id is blocked in search setup."""
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "sub/dir", # ID_PATTERN allows only [a-zA-Z0-9_-]
            "brief_notes": "notes",
            "jd_content": "jd"
        }
    )
    assert response.status_code == 422

def test_gem_refine_whitelist():
    """Test that only whitelisted GEM IDs can be refined."""
    # gem1 is whitelisted
    # We expect a 404 if it doesn't exist or 200 if it does,
    # but NOT a 403.
    # Since we don't want to actually run the LLM, we just check the whitelist logic.

    # gem99 is NOT whitelisted
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "gem99",
            "instruction": "make it better"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Unauthorized GEM ID"

def test_gem_refine_path_traversal():
    """Test path traversal in gem_id."""
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "../prompts/gem1",
            "instruction": "make it better"
        }
    )
    assert response.status_code == 422
