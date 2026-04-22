import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest
from infra.db.api import EntityUpdate, DiscardEntity

def test_pipeline_request_path_traversal():
    # Should reject malicious search_id
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../../evil", local_dir=".")

    # Should reject absolute local_dir
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="/etc/passwd")

    # Should reject relative path traversal local_dir
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="../evil")

    # Should accept valid inputs
    req = PipelineRequest(search_id="valid-search_123", local_dir="data/inputs")
    assert req.search_id == "valid-search_123"
    assert req.local_dir == "data/inputs"

def test_setup_search_path_traversal():
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="../../evil", brief_notes="test", jd_content="test")

    # Valid
    req = SetupSearchRequest(search_id="job-456", brief_notes="test", jd_content="test")
    assert req.search_id == "job-456"

def test_refine_request_path_traversal():
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../../evil", instruction="test")

    # Valid
    req = RefineRequest(gem_id="gem1", instruction="test")
    assert req.gem_id == "gem1"

def test_entity_update_path_traversal():
    with pytest.raises(ValidationError):
        EntityUpdate(
            entity_id="../../evil",
            current_stage="test",
            state="test",
            agent_responsible="test",
            trace_id="test"
        )

    # Valid
    req = EntityUpdate(
        entity_id="candidate-001",
        current_stage="test",
        state="test",
        agent_responsible="test",
        trace_id="test"
    )
    assert req.entity_id == "candidate-001"

def test_discard_entity_path_traversal():
    with pytest.raises(ValidationError):
        DiscardEntity(
            entity_id="../../evil",
            stage_at_discard="test",
            reason="test",
            agent_responsible="test",
            trace_id="test"
        )

    # Valid
    req = DiscardEntity(
        entity_id="candidate-002",
        stage_at_discard="test",
        reason="test",
        agent_responsible="test",
        trace_id="test"
    )
    assert req.entity_id == "candidate-002"
