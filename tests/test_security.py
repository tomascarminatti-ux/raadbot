import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest
from infra.db.api import EntityUpdate, DiscardEntity

def test_pipeline_request_path_traversal():
    # Should fail if local_dir contains ..
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="test", local_dir="../../etc/passwd")

    # Should fail if local_dir is absolute
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="test", local_dir="/etc/passwd")

def test_pipeline_request_search_id_injection():
    # Should fail if search_id contains invalid characters
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="test; drop table users", local_dir="runs/test")

def test_setup_search_request_validation():
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="invalid/id", brief_notes="notes", jd_content="jd")

def test_refine_request_validation():
    # Should fail if gem_id is not in allowed list
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="invalid_gem", instruction="refine")

    # Should fail if gem_id tries path traversal
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../config", instruction="refine")

def test_db_entity_update_validation():
    with pytest.raises(ValidationError):
        EntityUpdate(
            entity_id="id; injection",
            current_stage="stage",
            state="state",
            agent_responsible="agent",
            trace_id="trace"
        )

def test_db_discard_entity_validation():
    with pytest.raises(ValidationError):
        DiscardEntity(
            entity_id="id; injection",
            stage_at_discard="stage",
            reason="reason",
            agent_responsible="agent",
            trace_id="trace"
        )
