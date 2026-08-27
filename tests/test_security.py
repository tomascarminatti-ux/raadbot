import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_1", local_dir="inputs/search_1", candidate_id="cand_1"
    )
    assert req.search_id == "search_1"
    assert req.local_dir == "inputs/search_1"
    assert req.candidate_id == "cand_1"


def test_pipeline_request_invalid_identifiers():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../bad_search")
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="good_search", candidate_id="../../bad_candidate")
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)


def test_pipeline_request_invalid_local_dir():
    invalid_dirs = [
        "../etc",
        "..\\windows",
        "/etc/passwd",
        "C:\\Windows\\System32",
    ]
    for d in invalid_dirs:
        with pytest.raises(ValidationError) as excinfo:
            PipelineRequest(search_id="valid_search", local_dir=d)
        assert "Path traversal sequences are not allowed in local_dir" in str(
            excinfo.value
        )


def test_setup_search_request_valid():
    req = SetupSearchRequest(
        search_id="valid-search_123", brief_notes="notes", jd_content="jd"
    )
    assert req.search_id == "valid-search_123"


def test_setup_search_request_invalid_path_traversal():
    invalid_ids = [
        "../etc/passwd",
        "..\\windows\\system32",
        "search/../../id",
        "search_id; rm -rf /",
        "search id with spaces",
        "search#id",
    ]
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError) as excinfo:
            SetupSearchRequest(
                search_id=invalid_id, brief_notes="notes", jd_content="jd"
            )
        assert (
            "search_id must contain only alphanumeric characters, dashes, or underscores"
            in str(excinfo.value)
        )


def test_refine_request_valid():
    req = RefineRequest(gem_id="gem1", instruction="Refine prompt")
    assert req.gem_id == "gem1"


def test_refine_request_invalid_path_traversal():
    invalid_ids = [
        "../../etc/passwd",
        "gem1/../gem2",
        "gem1.md",
        "gem1\x00",
        "gem1\n",
    ]
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError) as excinfo:
            RefineRequest(gem_id=invalid_id, instruction="Refine prompt")
        assert (
            "gem_id must contain only alphanumeric characters, dashes, or underscores"
            in str(excinfo.value)
        )
