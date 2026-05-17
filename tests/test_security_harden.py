from fastapi.testclient import TestClient
from unittest.mock import patch
from api import app
from infra.db.api import app as db_app

client = TestClient(app)
db_client = TestClient(db_app)


def test_pipeline_request_validation():
    # Test invalid search_id
    response = client.post("/api/v1/run", json={
        "search_id": "../traversal",
        "local_dir": "data"
    })
    assert response.status_code == 422
    assert "search_id" in response.text

    # Test invalid local_dir (traversal)
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id",
        "local_dir": "../../etc"
    })
    assert response.status_code == 422
    assert "Invalid path" in response.text

    # Test invalid local_dir (absolute)
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id",
        "local_dir": "/etc"
    })
    assert response.status_code == 422
    assert "Invalid path" in response.text


def test_refine_request_validation():
    # Test invalid gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem!invalid",
        "instruction": "refine"
    })
    assert response.status_code == 422


def test_db_entity_upsert_validation():
    # Test invalid entity_id in DB API
    response = db_client.post("/entity/upsert", json={
        "entity_id": "id with spaces",
        "current_stage": "gem1",
        "state": "OK",
        "agent_responsible": "gem6",
        "trace_id": "valid-trace"
    })
    assert response.status_code == 422


def test_db_log_discovery_validation():
    # Test invalid agent_id in log_discovery
    response = db_client.post("/log/discovery", json={
        "entity_id": "valid-id",
        "agent_id": "agent/traversal",
        "input_ok": True,
        "output_ok": True,
        "time_ms": 100,
        "status": "OK",
        "trace_id": "valid-trace"
    })
    assert response.status_code == 422


@patch("api.run_pipeline")
def test_pipeline_error_masking(mock_run):
    mock_run.side_effect = Exception("Secret internal error details")
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id",
        "local_dir": "valid-dir"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Pipeline execution failed"
    assert "Secret internal error details" not in response.text


@patch("infra.db.api.get_db")
def test_db_error_masking(mock_get_db):
    mock_get_db.side_effect = Exception("SQL Injection Attempt or Database Down")
    response = db_client.post("/entity/upsert", json={
        "entity_id": "valid-id",
        "current_stage": "gem1",
        "state": "OK",
        "agent_responsible": "gem6",
        "trace_id": "valid-trace"
    })
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal database error during upsert"
    assert "SQL Injection Attempt" not in response.text
