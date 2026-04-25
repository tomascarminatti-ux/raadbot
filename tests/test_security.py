import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest
from infra.db.api import EntityUpdate, DiscardEntity


def test_pipeline_request_validation():
    # Valid
    PipelineRequest(search_id="valid-id_123")

    # Invalid - path traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../../etc/passwd")

    # Invalid - spaces
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="invalid id")

    # Invalid - candidate_id
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", candidate_id="; rm -rf /")


def test_setup_search_request_validation():
    # Valid
    SetupSearchRequest(search_id="project-alpha",
                       brief_notes="notes", jd_content="jd")

    # Invalid
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="project/../beta",
                           brief_notes="n", jd_content="j")


def test_refine_request_validation():
    # Valid
    RefineRequest(gem_id="gem1", instruction="better")

    # Invalid
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem1; drop table gems", instruction="attack")


def test_entity_update_validation():
    # Valid
    EntityUpdate(
        entity_id="candidate_42",
        current_stage="GEM1",
        state="PROCESSING",
        agent_responsible="agent_x",
        trace_id="trace_y"
    )

    # Invalid
    with pytest.raises(ValidationError):
        EntityUpdate(
            entity_id="path/../../traversal",
            current_stage="GEM1",
            state="PROCESSING",
            agent_responsible="agent_x",
            trace_id="trace_y"
        )


def test_discard_entity_validation():
    # Valid
    DiscardEntity(
        entity_id="candidate_99",
        stage_at_discard="GEM2",
        reason="low score",
        agent_responsible="agent_z",
        trace_id="trace_w"
    )

    # Invalid
    with pytest.raises(ValidationError):
        DiscardEntity(
            entity_id="id with symbols!",
            stage_at_discard="GEM2",
            reason="low score",
            agent_responsible="agent_z",
            trace_id="trace_w"
        )
