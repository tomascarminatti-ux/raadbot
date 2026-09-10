import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid_identifiers():
    req = PipelineRequest(
        search_id="search_123",
        candidate_id="cand-456",
        local_dir="data/inputs"
    )
    assert req.search_id == "search_123"
    assert req.candidate_id == "cand-456"
    assert req.local_dir == "data/inputs"


def test_pipeline_request_invalid_search_id_path_traversal():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../../etc/passwd")
    assert "search_id" in str(excinfo.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="valid_search", candidate_id="../secret_candidate"
        )
    assert "candidate_id" in str(excinfo.value)


def test_pipeline_request_invalid_local_dir_traversal():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="valid_search", local_dir="../relative/path"
        )
    assert "local_dir" in str(excinfo.value)


def test_pipeline_request_invalid_local_dir_absolute():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", local_dir="/etc/passwd")
    assert "local_dir" in str(excinfo.value)


def test_setup_search_request_validation():
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="search/../id", brief_notes="notes", jd_content="jd"
        )
    assert "search_id" in str(excinfo.value)


def test_refine_request_validation():
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="../../../gem1", instruction="refine")
    assert "gem_id" in str(excinfo.value)
