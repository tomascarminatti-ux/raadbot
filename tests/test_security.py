import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_path_traversal_protection():
    # Valid request
    valid_req = PipelineRequest(
        search_id="valid_search_123",
        candidate_id="cand_1",
        local_dir="data/inputs",
    )
    assert valid_req.search_id == "valid_search_123"
    assert valid_req.candidate_id == "cand_1"
    assert valid_req.local_dir == "data/inputs"

    # Invalid search_id with directory traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../../etc/passwd")

    # Invalid candidate_id with path traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", candidate_id="../candidate")

    # Invalid local_dir with relative directory traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="../secret_dir")

    # Invalid local_dir with absolute path
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="/etc/passwd")


def test_setup_search_request_path_traversal_protection():
    # Valid setup request
    req = SetupSearchRequest(
        search_id="search_ok",
        brief_notes="notes",
        jd_content="jd",
    )
    assert req.search_id == "search_ok"

    # Invalid search_id with path traversal
    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../../../tmp/malicious",
            brief_notes="notes",
            jd_content="jd",
        )


def test_refine_request_path_traversal_protection():
    # Valid refine request
    req = RefineRequest(gem_id="gem1", instruction="make it better")
    assert req.gem_id == "gem1"

    # Invalid gem_id with directory traversal attempt
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../../templates/dashboard", instruction="exploit")
