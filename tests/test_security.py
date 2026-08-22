import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH-123_abc",
        candidate_id="CAND-001",
        local_dir="runs/SEARCH-123/inputs",
    )
    assert req.search_id == "SEARCH-123_abc"
    assert req.candidate_id == "CAND-001"
    assert req.local_dir == "runs/SEARCH-123/inputs"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../invalid", local_dir="inputs")
    assert "search_id" in str(excinfo.value)
    assert "ID must contain only alphanumeric characters" in str(excinfo.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="VALID", candidate_id="../../etc/passwd", local_dir="inputs"
        )
    assert "candidate_id" in str(excinfo.value)


def test_pipeline_request_invalid_local_dir_traversal():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="VALID", local_dir="../secret_dir")
    assert "local_dir" in str(excinfo.value)
    assert "path traversal" in str(excinfo.value)


def test_pipeline_request_invalid_local_dir_absolute():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="VALID", local_dir="/etc/passwd")
    assert "local_dir" in str(excinfo.value)


def test_setup_search_request_invalid():
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="SEARCH/../DIR",
            brief_notes="notes",
            jd_content="jd",
        )
    assert "search_id" in str(excinfo.value)


def test_refine_request_invalid_gem_id():
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(
            gem_id="../../prompts/gem1",
            instruction="refine system prompt",
        )
    assert "gem_id" in str(excinfo.value)
