import pytest
from fastapi.testclient import TestClient
from api import app
import os
import shutil

client = TestClient(app, raise_server_exceptions=False)

def test_identifier_validation():
    # Test invalid search_id
    response = client.post("/api/v1/run", json={
        "search_id": "../../invalid",
        "local_dir": "tests"
    })
    assert response.status_code == 422

    # Test invalid gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem1; rm -rf /",
        "instruction": "test"
    })
    assert response.status_code == 422

def test_error_masking():
    # Trigger an error that would normally leak info (e.g. invalid model in background)
    # Actually, trigger_pipeline masks errors in the try/except block
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id",
        "model": "non-existent-model",
        "local_dir": "non-existent-dir"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Pipeline execution failed"
    # Ensure it doesn't contain "GeminiClient" or specific file paths
    assert "GeminiClient" not in str(response.json())
    assert "load_local_inputs" not in str(response.json())

def test_db_api_hardening():
    from infra.db.api import app as db_app
    db_client = TestClient(db_app, raise_server_exceptions=False)

    # Test invalid entity_id
    response = db_client.post("/entity/upsert", json={
        "entity_id": "bad' OR 1=1--",
        "current_stage": "GEM1",
        "state": "PENDING",
        "agent_responsible": "GEM1",
        "trace_id": "valid-trace"
    })
    assert response.status_code == 422

    # Test invalid trace_id
    response = db_client.post("/entity/upsert", json={
        "entity_id": "valid-id",
        "current_stage": "GEM1",
        "state": "PENDING",
        "agent_responsible": "GEM1",
        "trace_id": "invalid space"
    })
    assert response.status_code == 422

    # Test error masking in DB
    # (Mocking database failure if needed, but simple test for now)
    # If we send a valid model but something fails internally (e.g. db connection)
    # For now we just check the existing hardening
    pass

if __name__ == "__main__":
    # This is for manual run if needed
    pytest.main([__file__])
