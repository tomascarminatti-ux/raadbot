import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_path_traversal_prevention():
    # Valid request
    valid = PipelineRequest(
        search_id="search_123",
        local_dir="inputs/search_1",
        candidate_id="candidate-1",
    )
    assert valid.search_id == "search_123"
    assert valid.local_dir == "inputs/search_1"
    assert valid.candidate_id == "candidate-1"

    # Invalid search_id with directory traversal
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../../etc/passwd", local_dir="inputs/search_1")
    assert "Identifier must contain only alphanumeric" in str(exc_info.value)

    # Invalid candidate_id with path traversal
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", candidate_id="../candidate_1")
    assert "Identifier must contain only alphanumeric" in str(exc_info.value)

    # Invalid local_dir with relative traversal
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", local_dir="../../etc")
    assert "Path traversal or absolute paths are not allowed" in str(exc_info.value)

    # Invalid local_dir with absolute path
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", local_dir="/etc/passwd")
    assert "Path traversal or absolute paths are not allowed" in str(exc_info.value)


def test_setup_search_request_path_traversal_prevention():
    # Valid search_id
    valid = SetupSearchRequest(
        search_id="valid-search_99", brief_notes="notes", jd_content="jd"
    )
    assert valid.search_id == "valid-search_99"

    # Invalid search_id with directory traversal
    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="../invalid_id", brief_notes="notes", jd_content="jd"
        )
    assert "search_id must contain only alphanumeric" in str(exc_info.value)


def test_refine_request_path_traversal_prevention():
    # Valid gem_id
    valid = RefineRequest(gem_id="gem1", instruction="improve prompt")
    assert valid.gem_id == "gem1"

    # Invalid gem_id with directory traversal
    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(gem_id="../gem1", instruction="improve prompt")
    assert "gem_id must contain only alphanumeric" in str(exc_info.value)
