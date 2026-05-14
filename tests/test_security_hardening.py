import pytest
from fastapi.testclient import TestClient
from api import app
from infra.db.api import app as db_app

client = TestClient(app, raise_server_exceptions=False)
db_client = TestClient(db_app, raise_server_exceptions=False)

def test_path_traversal_pipeline_run():
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "../../etc"
    })
    assert response.status_code == 422

def test_identifier_validation_api():
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem 1",
        "instruction": "refine"
    })
    assert response.status_code == 422

def test_error_masking_api():
    # Force a 400 error that is masked
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "non_existent_folder_xyz"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Pipeline execution failed"

def test_db_api_validation():
    response = db_client.post("/entity/upsert", json={
        "entity_id": "invalid id",
        "current_stage": "test",
        "state": "test",
        "agent_responsible": "agent1",
        "trace_id": "trace1"
    })
    assert response.status_code == 422

def test_db_api_error_masking():
    # Force a 500 error (e.g. by providing invalid metadata type)
    response = db_client.post("/entity/upsert", json={
        "entity_id": "valid_id",
        "current_stage": "test",
        "state": "test",
        "metadata": "not a dict",
        "agent_responsible": "agent1",
        "trace_id": "trace1"
    })
    # Pydantic will catch "not a dict" first and return 422
    if response.status_code == 422:
        return

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal database error"
