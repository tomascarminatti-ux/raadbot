import pytest
from pydantic import ValidationError

from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="data/search_123",
        candidate_id="cand_456",
    )
    assert req.search_id == "search_123"
    assert req.candidate_id == "cand_456"
    assert req.local_dir == "data/search_123"


def test_pipeline_request_invalid_search_id_traversal():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="../etc/passwd",
            local_dir="data/search",
        )
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)


def test_pipeline_request_invalid_candidate_id_traversal():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="search_123",
            candidate_id="../../secret",
            local_dir="data/search",
        )
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)


def test_pipeline_request_invalid_local_dir_traversal():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="search_123",
            local_dir="data/../secret",
        )
    assert "local_dir cannot contain path traversal sequences" in str(excinfo.value)

    # Windows style backslash traversal check
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="search_123",
            local_dir="data\\..\\secret",
        )
    assert "local_dir cannot contain path traversal sequences" in str(excinfo.value)


def test_setup_search_request_traversal():
    req = SetupSearchRequest(
        search_id="valid-search_id-123",
        brief_notes="notes",
        jd_content="jd",
    )
    assert req.search_id == "valid-search_id-123"

    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="../../../etc/shadow",
            brief_notes="notes",
            jd_content="jd",
        )
    assert "search_id must contain only alphanumeric characters" in str(excinfo.value)


def test_refine_request_traversal():
    req = RefineRequest(gem_id="gem1", instruction="Improve clarity")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="gem1/../../etc/passwd", instruction="hack")
    assert "gem_id must contain only alphanumeric characters" in str(excinfo.value)
