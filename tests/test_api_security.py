import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="inputs/test_search",
        candidate_id="candidate_01"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "inputs/test_search"
    assert req.candidate_id == "candidate_01"


@pytest.mark.parametrize("invalid_id", [
    "../etc/passwd",
    "search/id",
    "search_123; rm -rf /",
    "search id",
    "search.id",
    "../../secret",
])
def test_pipeline_request_invalid_search_id(invalid_id):
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id=invalid_id, local_dir="valid_dir")
    assert "Invalid search_id" in str(exc_info.value)


@pytest.mark.parametrize("invalid_id", [
    "../candidate",
    "cand/id",
    "candidate.01",
    "cand 01",
])
def test_pipeline_request_invalid_candidate_id(invalid_id):
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", candidate_id=invalid_id, local_dir="valid_dir")
    assert "Invalid candidate_id" in str(exc_info.value)


@pytest.mark.parametrize("invalid_dir", [
    "../etc/passwd",
    "..\\windows\\system32",
    "/etc/passwd",
    "C:\\Windows\\System32",
    "some/dir/../../secret",
])
def test_pipeline_request_invalid_local_dir(invalid_dir):
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", local_dir=invalid_dir)
    assert "Invalid local_dir" in str(exc_info.value)


@pytest.mark.parametrize("invalid_id", [
    "../gem1",
    "gem1/sub",
    "gem1.md",
    "gem 1",
])
def test_refine_request_invalid_gem_id(invalid_id):
    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(gem_id=invalid_id, instruction="refine this")
    assert "Invalid gem_id" in str(exc_info.value)


def test_setup_search_request_invalid_search_id():
    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="../bad_search",
            brief_notes="notes",
            jd_content="jd"
        )
    assert "Invalid search_id" in str(exc_info.value)
