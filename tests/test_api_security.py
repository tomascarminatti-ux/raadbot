import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        candidate_id="candidate-abc",
        local_dir="data/inputs",
    )
    assert req.search_id == "search_123"
    assert req.candidate_id == "candidate-abc"
    assert req.local_dir == "data/inputs"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../invalid_id")
    assert "search_id" in str(excinfo.value) or "Identificador" in str(excinfo.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", candidate_id="cand/../../etc")
    assert "candidate_id" in str(excinfo.value) or "Identificador" in str(excinfo.value)


def test_pipeline_request_path_traversal_local_dir():
    invalid_dirs = [
        "../etc/passwd",
        "folder/../../secret",
        "/absolute/path",
        "C:\\Windows\\System32",
    ]
    for invalid_dir in invalid_dirs:
        with pytest.raises(ValidationError) as excinfo:
            PipelineRequest(search_id="valid_search", local_dir=invalid_dir)
        assert "local_dir" in str(excinfo.value) or "Ruta de directorio local" in str(excinfo.value)


def test_setup_search_request_validation():
    # Valid
    req = SetupSearchRequest(
        search_id="valid_search_1",
        brief_notes="notes",
        jd_content="jd",
    )
    assert req.search_id == "valid_search_1"

    # Invalid search_id with special characters
    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="search; DROP TABLE users;--",
            brief_notes="notes",
            jd_content="jd",
        )


def test_refine_request_validation():
    # Valid
    req = RefineRequest(gem_id="gem1", instruction="make it concise")
    assert req.gem_id == "gem1"

    # Invalid gem_id with path traversal
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../prompts/gem1", instruction="exploit")
