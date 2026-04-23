import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest
from infra.db.api import EntityUpdate, DiscardEntity


def test_pipeline_request_valid():
    req = PipelineRequest(search_id="valid-id_123", local_dir="runs/test")
    assert req.search_id == "valid-id_123"
    assert req.local_dir == "runs/test"


def test_pipeline_request_invalid_id():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="invalid/id", local_dir="runs/test")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="id; drop table users",
                        local_dir="runs/test")


def test_pipeline_request_path_traversal():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="../../etc/passwd")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="/absolute/path")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", drive_folder="..")


def test_setup_search_request_invalid_id():
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="invalid id",
                           brief_notes="notes", jd_content="jd")


def test_refine_request_invalid_id():
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem!1", instruction="improve")


def test_entity_update_invalid():
    with pytest.raises(ValidationError):
        EntityUpdate(
            entity_id="invalid/id",
            current_stage="stage",
            state="state",
            agent_responsible="agent",
            trace_id="trace"
        )

    with pytest.raises(ValidationError):
        EntityUpdate(
            entity_id="valid",
            current_stage="stage",
            state="state",
            agent_responsible="agent/malicious",
            trace_id="trace"
        )


def test_discard_entity_invalid():
    with pytest.raises(ValidationError):
        DiscardEntity(
            entity_id="valid",
            stage_at_discard="stage",
            reason="reason",
            agent_responsible="agent",
            trace_id="trace/traversal"
        )
