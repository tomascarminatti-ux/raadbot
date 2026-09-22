import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="inputs/search_123",
        candidate_id="cand_456"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "inputs/search_123"
    assert req.candidate_id == "cand_456"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="../invalid_search",
            local_dir="inputs/search_123"
        )
    assert "search_id" in str(exc_info.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="inputs/search_123",
            candidate_id="../../etc/passwd"
        )
    assert "candidate_id" in str(exc_info.value)


def test_pipeline_request_invalid_local_dir_traversal():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="../../etc"
        )
    assert "local_dir" in str(exc_info.value)


def test_pipeline_request_invalid_local_dir_absolute():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="/etc/passwd"
        )
    assert "local_dir" in str(exc_info.value)


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="valid_search_id",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "valid_search_id"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="invalid/search/id",
            brief_notes="notes",
            jd_content="jd"
        )


def test_refine_request_validation():
    req = RefineRequest(
        gem_id="gem1",
        instruction="Make it stricter"
    )
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(
            gem_id="../gem1",
            instruction="Make it stricter"
        )
