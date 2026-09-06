import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_path_traversal():
    # Valid request
    req = PipelineRequest(
        search_id="search_123", local_dir="data/inputs", candidate_id="cand_1"
    )
    assert req.search_id == "search_123"

    # Invalid search_id with path traversal
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../etc/passwd")
    assert "search_id" in str(exc_info.value)

    # Invalid candidate_id with special characters
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_id", candidate_id="cand/../1")
    assert "candidate_id" in str(exc_info.value)

    # Invalid local_dir with relative path traversal
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_id", local_dir="../secret_dir")
    assert "local_dir" in str(exc_info.value)

    # Invalid local_dir with absolute path
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_id", local_dir="/etc/passwd")
    assert "local_dir" in str(exc_info.value)


def test_setup_search_request_path_traversal():
    # Valid setup request
    req = SetupSearchRequest(
        search_id="search-01", brief_notes="notes", jd_content="jd"
    )
    assert req.search_id == "search-01"

    # Invalid search_id with directory traversal
    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="../../bad_search", brief_notes="notes", jd_content="jd"
        )
    assert "search_id" in str(exc_info.value)


def test_refine_request_path_traversal():
    # Valid refine request
    req = RefineRequest(gem_id="gem1", instruction="make it concise")
    assert req.gem_id == "gem1"

    # Invalid gem_id with path traversal attempt
    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(gem_id="../gem1", instruction="hack")
    assert "gem_id" in str(exc_info.value)
