import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from api import app, PipelineRequest, SetupSearchRequest, RefineRequest
from infra.db.api import EntityUpdate, DiscardEntity

client = TestClient(app)

def test_pipeline_request_validation():
    # Valid
    PipelineRequest(search_id="valid-id_123", local_dir="data/input")

    # Invalid search_id
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="invalid id!", local_dir="data")

    # Path traversal in local_dir
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="../secret")

    # Absolute path in local_dir
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="/etc/passwd")

def test_setup_search_request_validation():
    # Valid
    SetupSearchRequest(search_id="valid", brief_notes="notes", jd_content="jd")

    # Invalid search_id
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="id; drop table", brief_notes="n", jd_content="j")

def test_refine_request_validation():
    # Valid
    RefineRequest(gem_id="gem1", instruction="more strict")

    # Invalid gem_id (path traversal attempt)
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../config", instruction="test")

def test_db_entity_update_validation():
    # Valid
    EntityUpdate(
        entity_id="cand-001",
        current_stage="gem1",
        state="done",
        agent_responsible="gem1",
        trace_id="trace-123"
    )

    # Invalid entity_id
    with pytest.raises(ValidationError):
        EntityUpdate(
            entity_id="invalid!",
            current_stage="gem1",
            state="done",
            agent_responsible="gem1",
            trace_id="trace-123"
        )

def test_api_endpoints_security():
    # Verify 422 for path traversal in Refine GEM
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../.env",
        "instruction": "test"
    })
    assert response.status_code == 422

    # Verify 422 for path traversal in Pipeline Trigger
    response = client.post("/api/v1/run", json={
        "search_id": "valid",
        "local_dir": "../../etc"
    })
    assert response.status_code == 422
