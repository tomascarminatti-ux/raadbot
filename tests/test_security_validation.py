import pytest
from fastapi.testclient import TestClient
import os
import sys

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app
import config

client = TestClient(app)

def test_pipeline_request_id_validation():
    # Valid ID
    payload = {
        "search_id": "valid-id_123",
        "local_dir": "runs/test"
    }
    # Note: This might fail later in the function but should pass Pydantic validation
    # To just test validation, we can use the model directly
    from api import PipelineRequest
    PipelineRequest(**payload)

    # Invalid ID (path traversal)
    invalid_payload = {
        "search_id": "../etc/passwd",
        "local_dir": "runs/test"
    }
    with pytest.raises(ValueError, match="Invalid search_id format"):
        PipelineRequest(**invalid_payload)

def test_setup_search_request_id_validation():
    from api import SetupSearchRequest

    # Valid
    SetupSearchRequest(search_id="valid", brief_notes="notes", jd_content="jd")

    # Invalid
    with pytest.raises(ValueError, match="Invalid search_id format"):
        SetupSearchRequest(search_id="not valid!", brief_notes="notes", jd_content="jd")

def test_refine_request_gem_id_validation():
    from api import RefineRequest

    # Valid
    for gem in config.ALLOWED_GEMS:
        RefineRequest(gem_id=gem, instruction="better")

    # Invalid
    with pytest.raises(ValueError, match="Invalid gem_id"):
        RefineRequest(gem_id="gem6", instruction="hack")

def test_db_api_models_validation():
    from infra.db.api import EntityUpdate, DiscardEntity, DiscoveryLog

    # Valid
    EntityUpdate(
        entity_id="valid",
        current_stage="GEM1",
        state="PENDING",
        agent_responsible="gem1",
        trace_id="trace1"
    )

    # Invalid entity_id
    with pytest.raises(ValueError, match="Invalid format for field"):
        EntityUpdate(
            entity_id="invalid/id",
            current_stage="GEM1",
            state="PENDING",
            agent_responsible="gem1",
            trace_id="trace1"
        )

    # Invalid trace_id
    with pytest.raises(ValueError, match="Invalid format for field"):
        EntityUpdate(
            entity_id="valid",
            current_stage="GEM1",
            state="PENDING",
            agent_responsible="gem1",
            trace_id="trace space"
        )

def test_api_endpoints_rejection():
    # Test that FastAPI actually returns 422 for invalid Pydantic models
    response = client.post("/api/v1/run", json={"search_id": "../traversal", "local_dir": "."})
    assert response.status_code == 422

    response = client.post("/api/v1/search/setup", json={
        "search_id": "invalid space",
        "brief_notes": "notes",
        "jd_content": "jd"
    })
    assert response.status_code == 422

    response = client.post("/api/v1/gems/refine", json={"gem_id": "gem99", "instruction": "test"})
    assert response.status_code == 422
