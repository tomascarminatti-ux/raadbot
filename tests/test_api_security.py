import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid_identifiers():
    req = PipelineRequest(
        search_id="search-123_abc",
        candidate_id="cand_456-def",
        local_dir="valid/relative/path"
    )
    assert req.search_id == "search-123_abc"
    assert req.candidate_id == "cand_456-def"
    assert req.local_dir == "valid/relative/path"


@pytest.mark.parametrize("invalid_search_id", [
    "../etc/passwd",
    "search/123",
    "search_id; drop table users;",
    "search id",
    "search..id",
])
def test_pipeline_request_invalid_search_id(invalid_search_id):
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id=invalid_search_id)
    assert "search_id" in str(excinfo.value)


@pytest.mark.parametrize("invalid_candidate_id", [
    "../candidate",
    "candidate/123",
    "cand_id*",
])
def test_pipeline_request_invalid_candidate_id(invalid_candidate_id):
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", candidate_id=invalid_candidate_id)
    assert "candidate_id" in str(excinfo.value)


@pytest.mark.parametrize("invalid_local_dir", [
    "../secret_folder",
    "folder/../secret",
    "..\\secret",
    "/absolute/path/to/dir",
])
def test_pipeline_request_invalid_local_dir(invalid_local_dir):
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", local_dir=invalid_local_dir)
    assert "local_dir" in str(excinfo.value)


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="search_valid-1",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "search_valid-1"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../bad_id",
            brief_notes="notes",
            jd_content="jd"
        )


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="refine prompt")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../../prompts/secret", instruction="refine prompt")
