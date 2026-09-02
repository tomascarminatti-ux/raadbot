import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="data/search_123",
        candidate_id="cand_01"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "data/search_123"
    assert req.candidate_id == "cand_01"


def test_pipeline_request_path_traversal_search_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../../etc/passwd")
    assert "Identifier must contain only alphanumeric characters" in str(exc_info.value)


def test_pipeline_request_path_traversal_local_dir():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", local_dir="data/../../etc")
    assert "Directory traversal ('..') is strictly prohibited." in str(exc_info.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", candidate_id="../cand_01")
    assert "Identifier must contain only alphanumeric characters" in str(exc_info.value)


def test_setup_search_request_path_traversal():
    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="../evil_search",
            brief_notes="notes",
            jd_content="jd"
        )
    assert "search_id must contain only alphanumeric characters" in str(exc_info.value)


def test_refine_request_path_traversal():
    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(
            gem_id="../gem1",
            instruction="refine"
        )
    assert "gem_id must contain only alphanumeric characters" in str(exc_info.value)
