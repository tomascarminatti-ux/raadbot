import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest

def test_pipeline_request_valid_ids():
    req = PipelineRequest(search_id="valid_search_123", candidate_id="cand-01", local_dir="inputs/test")
    assert req.search_id == "valid_search_123"
    assert req.candidate_id == "cand-01"
    assert req.local_dir == "inputs/test"

def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../invalid_id")
    assert "search_id" in str(exc_info.value) or "ID contains invalid characters" in str(exc_info.value)

def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search1", candidate_id="cand/../../etc")

def test_pipeline_request_invalid_local_dir_traversal():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search1", local_dir="../../etc/passwd")

def test_pipeline_request_invalid_local_dir_absolute():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search1", local_dir="/etc/passwd")

def test_setup_search_request_invalid_search_id():
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="search_123; rm -rf /", brief_notes="notes", jd_content="jd")

def test_refine_request_invalid_gem_id():
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="make it concise")
