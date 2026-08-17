import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="valid/path",
        candidate_id="cand-1"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "valid/path"
    assert req.candidate_id == "cand-1"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../../etc/passwd", local_dir="valid/path")
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", candidate_id="../cand1")
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)


def test_pipeline_request_invalid_local_dir_traversal():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", local_dir="../secret_dir")
    assert "Path traversal or absolute paths are not allowed" in str(excinfo.value)


def test_pipeline_request_invalid_local_dir_absolute():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", local_dir="/etc/passwd")
    assert "Path traversal or absolute paths are not allowed" in str(excinfo.value)


def test_setup_search_request_invalid_search_id():
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="search/../traversal",
            brief_notes="notes",
            jd_content="jd"
        )
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)


def test_refine_request_invalid_gem_id():
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(
            gem_id="../../prompts/malicious",
            instruction="refine prompt"
        )
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)
