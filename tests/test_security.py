import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest
from infra.db.api import EntityUpdate, DiscardEntity


def test_pipeline_request_valid():
    # Should not raise any error
    PipelineRequest(search_id="valid-id_123", local_dir="inputs/search1")


def test_pipeline_request_invalid_id():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="invalid id!")
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="id;DROP TABLE users")
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../../etc/passwd")


def test_pipeline_request_path_traversal():
    with pytest.raises(ValidationError, match="cannot contain '..'"):
        PipelineRequest(search_id="valid", local_dir="../outside")
    with pytest.raises(ValidationError, match="must be a relative path"):
        PipelineRequest(search_id="valid", local_dir="/etc/passwd")


def test_setup_search_invalid_id():
    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="!!!", brief_notes="...", jd_content="...")


def test_refine_request_invalid_id():
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem space", instruction="...")


def test_entity_update_invalid_ids():
    valid_data = {
        "entity_id": "valid",
        "current_stage": "gem1",
        "state": "active",
        "agent_responsible": "agent1",
        "trace_id": "trace1"
    }
    # Test entity_id
    with pytest.raises(ValidationError):
        EntityUpdate(**{**valid_data, "entity_id": "invalid!"})
    # Test agent_responsible
    with pytest.raises(ValidationError):
        EntityUpdate(**{**valid_data, "agent_responsible": "agent space"})
    # Test trace_id
    with pytest.raises(ValidationError):
        EntityUpdate(**{**valid_data, "trace_id": "trace;injection"})


def test_discard_entity_invalid_ids():
    valid_data = {
        "entity_id": "valid",
        "stage_at_discard": "gem1",
        "reason": "low score",
        "agent_responsible": "agent1",
        "trace_id": "trace1"
    }
    with pytest.raises(ValidationError):
        DiscardEntity(**{**valid_data, "entity_id": "invalid!"})
