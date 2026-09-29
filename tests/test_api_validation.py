import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="data/search_123",
        candidate_id="cand_456"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "data/search_123"
    assert req.candidate_id == "cand_456"


def test_pipeline_request_invalid_identifiers():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../invalid_search")
    assert "Identifier must contain only alphanumeric characters" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="search_123", candidate_id="cand/../../etc")
    assert "Identifier must contain only alphanumeric characters" in str(exc_info.value)


def test_pipeline_request_path_traversal_local_dir():
    traversal_paths = [
        "../secret_folder",
        "..\\secret_folder",
        "data/../../etc/passwd",
        "/etc/passwd",
        "C:\\Windows\\System32"
    ]
    for path in traversal_paths:
        with pytest.raises(ValidationError) as exc_info:
            PipelineRequest(search_id="valid_search", local_dir=path)
        assert "Path traversal or absolute paths are not allowed" in str(exc_info.value)


def test_setup_search_request_validation():
    # Valid
    req = SetupSearchRequest(
        search_id="search_789",
        brief_notes="Briefing notes",
        jd_content="JD text"
    )
    assert req.search_id == "search_789"

    # Invalid
    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="search/../789",
            brief_notes="Notes",
            jd_content="JD"
        )
    assert "search_id must contain only alphanumeric characters" in str(exc_info.value)


def test_refine_request_validation():
    # Valid
    req = RefineRequest(gem_id="gem1", instruction="Improve clarity")
    assert req.gem_id == "gem1"

    # Invalid - path traversal vector
    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(gem_id="../gem1", instruction="Improve clarity")
    assert "gem_id must contain only alphanumeric characters" in str(exc_info.value)
