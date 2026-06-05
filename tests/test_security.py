import pytest
from fastapi.testclient import TestClient
from api import app
import config
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_pipeline_request_validation():
    # Valid request
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id_123",
        "local_dir": "test_data"
    })
    # Should fail because local_dir doesn't exist or API key missing,
    # but we are looking for Pydantic validation error (422) vs 400.
    assert response.status_code != 422

    # Invalid search_id (path traversal attempt)
    response = client.post("/api/v1/run", json={
        "search_id": "../traversal",
        "local_dir": "test_data"
    })
    assert response.status_code == 422
    assert "search_id" in response.json()["detail"][0]["loc"]

def test_refine_gem_whitelisting():
    # Attempt to refine a non-whitelisted GEM
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "invalid_gem",
        "instruction": "refine it"
    })
    assert response.status_code == 403
    assert "Access to this GEM is restricted" in response.json()["detail"]

    # Attempt path traversal via gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../secrets",
        "instruction": "refine it"
    })
    assert response.status_code == 422

def test_error_leakage_prevention():
    with patch("api.run_pipeline", side_effect=Exception("Database password is 'secret123'")):
        response = client.post("/api/v1/run", json={
            "search_id": "valid-id",
            "local_dir": "test_data"
        })
        assert response.status_code == 400
        assert "Database password" not in response.json()["detail"]
        assert "An error occurred while processing the pipeline request." in response.json()["detail"]
