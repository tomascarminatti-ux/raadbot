
import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest
from infra.db.api import EntityUpdate

def test_pipeline_request_path_traversal():
    # Test search_id with path traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../../etc/passwd", local_dir="data")

def test_setup_search_path_traversal():
    # Test search_id with path traversal
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="sub/../../etc", brief_notes="notes", jd_content="jd")

def test_refine_request_path_traversal():
    # Test gem_id with path traversal
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../api", instruction="make it better")

def test_entity_update_path_traversal():
    # Test entity_id with path traversal
    with pytest.raises(ValidationError):
        EntityUpdate(
            entity_id="../../../bad",
            current_stage="gem1",
            state="active",
            agent_responsible="agent",
            trace_id="123"
        )

def test_pipeline_request_local_dir_traversal():
    # Test local_dir with path traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="/etc")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="../secrets")
