import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_path_traversal():
    """Verify that search_id, candidate_id, and local_dir reject path traversal payloads."""
    # Invalid search_id
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../evil")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search/123")

    # Invalid candidate_id
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search1", candidate_id="../../etc/passwd")

    # Invalid local_dir
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search1", local_dir="../secret_dir")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search1", local_dir="/etc/passwd")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search1", local_dir="C:\\Windows\\System32")

    # Valid inputs
    valid = PipelineRequest(
        search_id="valid_search-123",
        candidate_id="cand_123",
        local_dir="valid_dir/subdir",
    )
    assert valid.search_id == "valid_search-123"
    assert valid.candidate_id == "cand_123"
    assert valid.local_dir == "valid_dir/subdir"


def test_setup_search_request_path_traversal():
    """Verify that SetupSearchRequest rejects invalid search_id values."""
    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../invalid_id", brief_notes="test", jd_content="test"
        )

    valid = SetupSearchRequest(
        search_id="valid_search_1", brief_notes="test", jd_content="test"
    )
    assert valid.search_id == "valid_search_1"


def test_refine_request_path_traversal():
    """Verify that RefineRequest restricts gem_id to valid GEM identifiers."""
    # Path traversal payload
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../../../etc/passwd", instruction="test")

    # Arbitrary file payload
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem6", instruction="test")

    # Valid GEM ID
    valid = RefineRequest(gem_id="gem3", instruction="Make prompt clearer")
    assert valid.gem_id == "gem3"
