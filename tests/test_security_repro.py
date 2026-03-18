import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from api import app

client = TestClient(app)

@pytest.fixture
def mock_gemini():
    with patch("api.GeminiClient") as mock:
        instance = mock.return_value
        instance.run_gem.return_value = {"markdown": "Refined prompt", "data": {}}
        yield instance

def test_pipeline_run_invalid_search_id():
    payload = {
        "search_id": "../traversal",
        "local_dir": "runs/test"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    # Pydantic 2 error message contains info about the pattern mismatch
    assert "pattern" in response.text

def test_pipeline_run_valid_search_id():
    # We mock run_pipeline to avoid actual execution
    with patch("api.run_pipeline") as mock_run:
        mock_run.return_value = {"status": "success", "search_id": "valid-id", "output_dir": "runs/valid-id", "summary": {}}
        payload = {
            "search_id": "valid-id",
            "local_dir": "runs/test"
        }
        response = client.post("/api/v1/run", json=payload)
        assert response.status_code == 200

def test_refine_gem_path_traversal(mock_gemini):
    payload = {
        "gem_id": "../README",
        "instruction": "Refine it"
    }
    # Should be caught by Pydantic pattern validation
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422

def test_refine_gem_valid_id(mock_gemini):
    # Ensure prompts/gem1.md exists for the test
    import os
    os.makedirs("prompts", exist_ok=True)
    with open("prompts/gem1.md", "w") as f:
        f.write("test prompt")

    payload = {
        "gem_id": "gem1",
        "instruction": "Refine it"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_error_leakage_pipeline():
    with patch("api.run_pipeline", side_effect=Exception("Sensitive database path: /etc/passwd")):
        payload = {
            "search_id": "valid-id",
            "local_dir": "runs/test"
        }
        response = client.post("/api/v1/run", json=payload)
        assert response.status_code == 400
        assert "Error starting the pipeline" in response.json()["detail"]
        assert "/etc/passwd" not in response.json()["detail"]

from infra.db.api import app as db_app
db_client = TestClient(db_app)

def test_db_upsert_invalid_id():
    payload = {
        "entity_id": "invalid/id",
        "current_stage": "GEM1",
        "state": "PENDING",
        "agent_responsible": "gem1",
        "trace_id": "trace1"
    }
    response = db_client.post("/entity/upsert", json=payload)
    assert response.status_code == 422

def test_db_error_leakage():
    with patch("infra.db.api.get_db", side_effect=Exception("Table 'secret' not found in /private/db.sqlite")):
        payload = {
            "entity_id": "valid-id",
            "current_stage": "GEM1",
            "state": "PENDING",
            "agent_responsible": "gem1",
            "trace_id": "trace1"
        }
        response = db_client.post("/entity/upsert", json=payload)
        assert response.status_code == 500
        assert "Internal database error" in response.json()["detail"]
        assert "/private/db.sqlite" not in response.json()["detail"]
