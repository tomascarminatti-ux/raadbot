from fastapi.testclient import TestClient
from api import app
import os
import pytest
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_refine_gem_path_traversal_blocked():
    # Attempt to read/write a file outside of prompts/
    payload = {
        "gem_id": "../traversal_test_file",
        "instruction": "Overwrite with malicious content"
    }

    response = client.post("/api/v1/gems/refine", json=payload)
    # Pydantic regex pattern r"^[a-zA-Z0-9_-]+$" should block "../"
    assert response.status_code == 422

def test_refine_gem_whitelist_blocked():
    payload = {
        "gem_id": "non_existent_gem",
        "instruction": "something"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    # Regex allows this, but whitelist should block it
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid GEM ID"

def test_pipeline_local_dir_traversal_blocked():
    payload = {
        "search_id": "test-search",
        "local_dir": "/etc/passwd",
        "model": "gemini-2.0-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    # Check that the error message mentions our validation
    errors = response.json()["detail"]
    assert any("Invalid local_dir path" in err["msg"] for err in errors)

def test_pipeline_invalid_search_id_blocked():
    payload = {
        "search_id": "search id with spaces",
        "local_dir": "data",
        "model": "gemini-2.0-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_db_api_invalid_entity_id_blocked():
    from infra.db.api import app as db_app
    db_client = TestClient(db_app)

    payload = {
        "entity_id": "bad; id",
        "current_stage": "gem1",
        "state": "active",
        "agent_responsible": "gem1",
        "trace_id": "trace1"
    }
    response = db_client.post("/entity/upsert", json=payload)
    assert response.status_code == 422
