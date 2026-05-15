
from fastapi.testclient import TestClient
import pytest
from api import app as main_app
from infra.db.api import app as db_app

main_client = TestClient(main_app)
db_client = TestClient(db_app)

def test_main_api_harden():
    # Test search_id validation
    response = main_client.post("/api/v1/run", json={
        "search_id": "../traversal",
        "local_dir": "test"
    })
    assert response.status_code == 422

    response = main_client.post("/api/v1/search/setup", json={
        "search_id": "invalid; injection",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422

    # Test gem_id validation
    response = main_client.post("/api/v1/gems/refine", json={
        "gem_id": "gem1; rm -rf /",
        "instruction": "test"
    })
    assert response.status_code == 422

def test_db_api_harden():
    # Test entity_id validation
    response = db_client.post("/entity/upsert", json={
        "entity_id": "drop table entity_state",
        "current_stage": "GEM1",
        "state": "PENDING",
        "agent_responsible": "GEM1",
        "trace_id": "abc-123"
    })
    assert response.status_code == 422

    # Test discovery log validation
    response = db_client.post("/log/discovery", json={
        "entity_id": "valid-id",
        "agent_id": "invalid id",
        "trace_id": "valid_trace"
    })
    assert response.status_code == 422

def test_error_masking():
    # We trigger an error in main_app and check if detail is masked
    # For example, calling /api/v1/run without providing drive_folder or local_dir
    # will raise a ValueError in run_pipeline, which is caught and re-raised as HTTPException(400)
    response = main_client.post("/api/v1/run", json={
        "search_id": "valid_id"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Pipeline execution failed"

if __name__ == "__main__":
    pytest.main([__file__])
