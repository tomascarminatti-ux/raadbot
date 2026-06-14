
import pytest
from fastapi.testclient import TestClient
from api import app
import config
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_refine_gem_path_traversal():
    """Verify that path traversal in gem_id is rejected by Pydantic pattern or logic."""
    # Attempting traversal
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../README",
        "instruction": "test"
    })
    # Pydantic Field(pattern=...) should catch this if it contains dots or slashes
    assert response.status_code == 422  # Unprocessable Entity (Validation Error)

def test_refine_gem_unauthorized_whitelist():
    """Verify that valid IDs not in whitelist are rejected."""
    # 'secret_config' follows pattern but not in config.ALLOWED_GEMS
    with patch("config.ALLOWED_GEMS", ["gem1"]):
        response = client.post("/api/v1/gems/refine", json={
            "gem_id": "secret_config",
            "instruction": "test"
        })
        assert response.status_code == 403
        assert response.json()["detail"] == "Unauthorized GEM access"

def test_pipeline_run_path_traversal():
    """Verify that path traversal in search_id is rejected."""
    response = client.post("/api/v1/run", json={
        "search_id": "../../etc/passwd",
        "local_dir": "test"
    })
    assert response.status_code == 422

def test_setup_search_path_traversal():
    """Verify that path traversal in search_id is rejected in setup."""
    response = client.post("/api/v1/search/setup", json={
        "search_id": "traversal/test",
        "brief_notes": "notes",
        "jd_content": "jd"
    })
    assert response.status_code == 422

@patch("api.run_pipeline")
def test_pipeline_error_no_leak(mock_run):
    """Verify that internal errors don't leak details."""
    mock_run.side_effect = Exception("Sensitive database error details")
    response = client.post("/api/v1/run", json={
        "search_id": "VALID-ID-123",
        "local_dir": "test"
    })
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error during pipeline execution"
    assert "Sensitive" not in response.text

def test_list_gems_uses_whitelist():
    """Verify list_gems only returns what is allowed."""
    with patch("config.ALLOWED_GEMS", ["gem1"]):
        response = client.get("/api/v1/gems")
        assert response.status_code == 200
        data = response.json()
        ids = [g["id"] for g in data]
        assert ids == ["gem1"]
