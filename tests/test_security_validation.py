from fastapi.testclient import TestClient
from api import app
import config

client = TestClient(app)


def test_pipeline_request_path_traversal():
    """Test that search_id with path traversal characters is rejected."""
    payload = {
        "search_id": "../../etc/passwd",
        "local_dir": "runs/test/inputs"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text


def test_pipeline_request_valid_id():
    """Test that a valid search_id passes validation (even if backend fails later)."""
    payload = {
        "search_id": "valid-search-123",
        "local_dir": "non_existent_dir"
    }
    # This should pass Pydantic validation but might fail in run_pipeline
    response = client.post("/api/v1/run", json=payload)
    # If it reached run_pipeline, it might return 400 with our new safe message
    # or 422 if it's still validation error from other fields.
    # The point is it didn't fail with path traversal.
    assert response.status_code != 422 or "search_id" not in response.text


def test_refine_request_invalid_gem():
    """Test that invalid gem_id is rejected."""
    payload = {
        "gem_id": "invalid_gem",
        "instruction": "make it better"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "Invalid gem_id" in response.text


def test_refine_request_path_traversal():
    """Test that path traversal in gem_id is rejected."""
    payload = {
        "gem_id": "../config.py",
        "instruction": "overwrite"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422


def test_list_gems_uses_whitelist():
    """Test that list_gems only returns allowed gems."""
    response = client.get("/api/v1/gems")
    assert response.status_code == 200
    data = response.json()
    gem_ids = [g["id"] for g in data]
    assert all(gid in config.ALLOWED_GEMS for gid in gem_ids)
    assert "gem1" in gem_ids


def test_db_api_validation():
    """Test validation in the DB API."""
    from infra.db.api import app as db_app
    db_client = TestClient(db_app)

    # Test entity upsert with bad ID
    payload = {
        "entity_id": "bad/id",
        "current_stage": "test",
        "state": "active",
        "agent_responsible": "test_agent",
        "trace_id": "trace1"
    }
    response = db_client.post("/entity/upsert", json=payload)
    assert response.status_code == 422

    # Test discovery log with bad trace ID
    payload = {
        "entity_id": "valid_id",
        "agent_responsible": "test_agent",
        "trace_id": "bad/trace"
    }
    response = db_client.post("/log/discovery", json=payload)
    assert response.status_code == 422
