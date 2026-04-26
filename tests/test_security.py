import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest
from infra.db.api import EntityUpdate, DiscardEntity

def test_pipeline_request_path_traversal():
    invalid_ids = ["../traversal", "../../etc/passwd", "subdir/id", "id; rm -rf /", "id\nnewline"]
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id=invalid_id, local_dir=".")

        with pytest.raises(ValidationError):
            PipelineRequest(search_id="valid", candidate_id=invalid_id, local_dir=".")

def test_setup_search_request_path_traversal():
    invalid_ids = ["../traversal", "path/to/something", "!!invalid!!"]
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            SetupSearchRequest(search_id=invalid_id, brief_notes="test", jd_content="test")

def test_refine_request_path_traversal():
    invalid_ids = ["../gem", "prompts/gem1", "gem1.md"]
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            RefineRequest(gem_id=invalid_id, instruction="test")

def test_db_entity_update_path_traversal():
    invalid_ids = ["../entity", "secret/id", "id' OR '1'='1"]
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            EntityUpdate(
                entity_id=invalid_id,
                current_stage="test",
                state="test",
                agent_responsible="test",
                trace_id="test"
            )

def test_db_discard_entity_path_traversal():
    invalid_ids = ["../entity", "some\\path", "id&whoami"]
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            DiscardEntity(
                entity_id=invalid_id,
                stage_at_discard="test",
                reason="test",
                agent_responsible="test",
                trace_id="test"
            )

def test_valid_identifiers():
    valid_ids = ["valid-id", "valid_id_123", "id", "SEARCH-2026-002"]
    for valid_id in valid_ids:
        # Should NOT raise ValidationError
        PipelineRequest(search_id=valid_id, local_dir=".")
        SetupSearchRequest(search_id=valid_id, brief_notes="test", jd_content="test")
        RefineRequest(gem_id=valid_id, instruction="test")
        EntityUpdate(
            entity_id=valid_id,
            current_stage="test",
            state="test",
            agent_responsible="test",
            trace_id="test"
        )
        DiscardEntity(
            entity_id=valid_id,
            stage_at_discard="test",
            reason="test",
            agent_responsible="test",
            trace_id="test"
        )
