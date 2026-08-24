import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_path_traversal():
    # Valid request
    req = PipelineRequest(search_id="valid_search_123", local_dir="data/inputs")
    assert req.search_id == "valid_search_123"
    assert req.local_dir == "data/inputs"

    # Path traversal in search_id
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../etc/passwd")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search/id")

    # Path traversal in candidate_id
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", candidate_id="../../secret")

    # Path traversal in local_dir
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="../secret_dir")

    # Absolute path in local_dir
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="/etc/passwd")


def test_setup_search_request_path_traversal():
    req = SetupSearchRequest(
        search_id="valid_search", brief_notes="notes", jd_content="jd"
    )
    assert req.search_id == "valid_search"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../bad_path", brief_notes="notes", jd_content="jd"
        )


def test_refine_request_path_traversal():
    req = RefineRequest(gem_id="gem1", instruction="make it better")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../config", instruction="hack")

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem1; rm -rf /", instruction="hack")
