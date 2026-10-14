import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest

def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="valid/path_name",
        candidate_id="cand_456"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "valid/path_name"
    assert req.candidate_id == "cand_456"

def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../invalid_search", local_dir="valid/path")

def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_search", candidate_id="cand/../bad")

def test_pipeline_request_invalid_local_dir():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_search", local_dir="../secret_dir")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_search", local_dir="/etc/passwd")

def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="valid_search_1",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "valid_search_1"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="bad/search/id",
            brief_notes="notes",
            jd_content="jd"
        )

def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="make it better")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem1/../gem2", instruction="hack")
