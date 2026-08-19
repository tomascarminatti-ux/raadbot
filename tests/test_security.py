import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_path_traversal_validation():
    # Test valid search_id and candidate_id
    req = PipelineRequest(search_id="search_123", candidate_id="cand-01", local_dir="inputs/search1")
    assert req.search_id == "search_123"
    assert req.candidate_id == "cand-01"
    assert req.local_dir == "inputs/search1"

    # Test path traversal in search_id
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../etc/passwd", local_dir="inputs/search1")
    assert "search_id" in str(excinfo.value)

    # Test path traversal in candidate_id
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", candidate_id="../../secret")
    assert "candidate_id" in str(excinfo.value)

    # Test directory traversal in local_dir
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", local_dir="../secret_dir")
    assert "local_dir" in str(excinfo.value)

    # Test Windows style directory traversal in local_dir
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", local_dir="..\\secret_dir")
    assert "local_dir" in str(excinfo.value)

    # Test absolute path in local_dir
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", local_dir="/etc/passwd")
    assert "local_dir" in str(excinfo.value)


def test_setup_search_request_validation():
    # Valid request
    req = SetupSearchRequest(search_id="search_abc-1", brief_notes="notes", jd_content="jd")
    assert req.search_id == "search_abc-1"

    # Invalid search_id with path traversal
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(search_id="../../../etc", brief_notes="notes", jd_content="jd")
    assert "search_id" in str(excinfo.value)


def test_refine_request_validation():
    # Valid request
    req = RefineRequest(gem_id="gem1", instruction="make it shorter")
    assert req.gem_id == "gem1"

    # Invalid gem_id with path traversal
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="../../prompts/malicious", instruction="hack")
    assert "gem_id" in str(excinfo.value)
