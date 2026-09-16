import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest

def test_pipeline_request_path_traversal_validation():
    # Valid identifiers and paths
    req = PipelineRequest(search_id="SEARCH-123", candidate_id="CAND-001", local_dir="data/inputs")
    assert req.search_id == "SEARCH-123"
    assert req.candidate_id == "CAND-001"
    assert req.local_dir == "data/inputs"

    # Invalid search_id with path traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../etc/passwd")

    # Invalid candidate_id with path traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="SEARCH-123", candidate_id="../../secret")

    # Invalid local_dir with relative path traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="SEARCH-123", local_dir="../secret_dir")

    # Invalid local_dir with absolute path
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="SEARCH-123", local_dir="/etc/passwd")


def test_setup_search_request_validation():
    # Valid request
    req = SetupSearchRequest(search_id="SEARCH_001", brief_notes="notes", jd_content="jd")
    assert req.search_id == "SEARCH_001"

    # Invalid search_id
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="SEARCH/../../001", brief_notes="notes", jd_content="jd")


def test_refine_request_validation():
    # Valid request
    req = RefineRequest(gem_id="gem1", instruction="make concise")
    assert req.gem_id == "gem1"

    # Invalid gem_id path traversal
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="make concise")
