import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid_identifiers():
    req = PipelineRequest(
        search_id="valid_search-123",
        candidate_id="cand_1",
        local_dir="valid/relative/path",
    )
    assert req.search_id == "valid_search-123"
    assert req.candidate_id == "cand_1"
    assert req.local_dir == "valid/relative/path"


def test_pipeline_request_path_traversal_search_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../../etc/passwd")
    assert "Invalid identifier" in str(exc_info.value)


def test_pipeline_request_path_traversal_local_dir():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_id", local_dir="../secret")
    assert "path traversal" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_id", local_dir="/etc/passwd")
    assert "path traversal" in str(exc_info.value)


def test_setup_search_request_path_traversal():
    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="search/../traversal",
            brief_notes="notes",
            jd_content="jd",
        )
    assert "Invalid identifier" in str(exc_info.value)


def test_refine_request_path_traversal():
    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(gem_id="../config", instruction="refine")
    assert "Invalid identifier" in str(exc_info.value)

    valid_req = RefineRequest(gem_id="gem1", instruction="refine")
    assert valid_req.gem_id == "gem1"
