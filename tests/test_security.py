import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH-123",
        local_dir="runs/SEARCH-123/inputs",
        candidate_id="cand_456"
    )
    assert req.search_id == "SEARCH-123"
    assert req.local_dir == "runs/SEARCH-123/inputs"
    assert req.candidate_id == "cand_456"


def test_pipeline_request_path_traversal_local_dir():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="../etc/passwd"
        )
    assert "Path traversal or absolute paths are not allowed" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="runs/../../secret"
        )
    assert "Path traversal or absolute paths are not allowed" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="/etc/passwd"
        )
    assert "Path traversal or absolute paths are not allowed" in str(exc_info.value)


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="SEARCH/../123",
            local_dir="runs/inputs"
        )
    assert "Must contain only alphanumeric characters, dashes, and underscores" in str(exc_info.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="SEARCH_123",
            candidate_id="cand; drop table candidates;"
        )
    assert "Must contain only alphanumeric characters, dashes, and underscores" in str(exc_info.value)


def test_setup_search_request_validation():
    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="search_id_with_space ",
            brief_notes="notes",
            jd_content="jd"
        )
    assert "Must contain only alphanumeric characters, dashes, and underscores" in str(exc_info.value)


def test_refine_request_validation():
    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(
            gem_id="../../etc/passwd",
            instruction="Make it better"
        )
    assert "Must contain only alphanumeric characters, dashes, and underscores" in str(exc_info.value)
