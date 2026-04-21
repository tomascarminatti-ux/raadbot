import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest
from infra.db.api import EntityUpdate, DiscardEntity

def test_pipeline_request_path_traversal():
    # Test search_id
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../evil", local_dir="tests")
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="/etc/passwd", local_dir="tests")

    # Test candidate_id
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", candidate_id="../evil", local_dir="tests")

    # Test local_dir
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="/etc")
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="../secret")

def test_setup_search_request_path_traversal():
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="../evil", brief_notes="test", jd_content="test")

def test_refine_request_path_traversal():
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../evil", instruction="test")
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem1/../../etc/passwd", instruction="test")

def test_db_entity_update_path_traversal():
    with pytest.raises(ValidationError):
        EntityUpdate(
            entity_id="../evil",
            current_stage="test",
            state="test",
            agent_responsible="test",
            trace_id="test"
        )

def test_db_discard_entity_path_traversal():
    with pytest.raises(ValidationError):
        DiscardEntity(
            entity_id="../evil",
            stage_at_discard="test",
            reason="test",
            agent_responsible="test",
            trace_id="test"
        )
