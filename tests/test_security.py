import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH-123",
        local_dir="data/search_1",
        candidate_id="cand_456"
    )
    assert req.search_id == "SEARCH-123"
    assert req.local_dir == "data/search_1"
    assert req.candidate_id == "cand_456"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="../etc/passwd",
            local_dir="data/search_1"
        )
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="SEARCH-123",
            candidate_id="cand/../../secret"
        )
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)


def test_pipeline_request_path_traversal_local_dir():
    invalid_paths = [
        "../secret_dir",
        "data/../../etc",
        "/etc/passwd",
        "C:\\Windows\\System32",
        "..\\relative\\path"
    ]
    for path in invalid_paths:
        with pytest.raises(ValidationError) as excinfo:
            PipelineRequest(
                search_id="SEARCH-123",
                local_dir=path
            )
        assert "Invalid local_dir" in str(excinfo.value)


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="VALID-ID-1",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "VALID-ID-1"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="invalid/path",
            brief_notes="notes",
            jd_content="jd"
        )


def test_refine_request_validation():
    req = RefineRequest(
        gem_id="gem1",
        instruction="make it concise"
    )
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(
            gem_id="../gem1",
            instruction="make it concise"
        )
