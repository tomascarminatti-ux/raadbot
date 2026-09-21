import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest

def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH-123_abc",
        candidate_id="candidate_1",
        local_dir="valid/path/dir"
    )
    assert req.search_id == "SEARCH-123_abc"
    assert req.candidate_id == "candidate_1"
    assert req.local_dir == "valid/path/dir"

def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../../etc/passwd", local_dir="valid/dir")
    assert "search_id" in str(exc_info.value) or "Identifier must contain" in str(exc_info.value)

def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", candidate_id="../invalid")

def test_pipeline_request_invalid_local_dir_traversal():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="../secret")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="foo/../bar")

def test_pipeline_request_invalid_local_dir_absolute():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="/etc/passwd")

def test_setup_search_request_validation():
    # Valid
    req = SetupSearchRequest(
        search_id="valid-id_123",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "valid-id_123"

    # Invalid search_id with path traversal or invalid characters
    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="invalid/id",
            brief_notes="notes",
            jd_content="jd"
        )

def test_refine_request_validation():
    # Valid
    req = RefineRequest(gem_id="gem1", instruction="make it better")
    assert req.gem_id == "gem1"

    # Invalid gem_id path traversal attempt
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem1/../../secret", instruction="hack")
