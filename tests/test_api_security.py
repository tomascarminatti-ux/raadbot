import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_path_traversal_validation():
    # Valid request should not raise exception
    req = PipelineRequest(
        search_id="SEARCH-001",
        candidate_id="CANDIDATE_123",
        local_dir="inputs/search_001"
    )
    assert req.search_id == "SEARCH-001"
    assert req.candidate_id == "CANDIDATE_123"
    assert req.local_dir == "inputs/search_001"

    # Path traversal in search_id
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../../etc/passwd")
    assert "Identifier must contain only alphanumeric" in str(exc_info.value)

    # Path traversal in candidate_id
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="SEARCH-001", candidate_id="../secret")
    assert "Identifier must contain only alphanumeric" in str(exc_info.value)

    # Path traversal in local_dir with '..'
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="SEARCH-001", local_dir="../secret_folder")
    assert "local_dir contains unsafe path traversal" in str(exc_info.value)

    # Absolute path in local_dir
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="SEARCH-001", local_dir="/etc/passwd")
    assert "local_dir contains unsafe path traversal" in str(exc_info.value)

    # Windows drive path in local_dir
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="SEARCH-001", local_dir="C:\\Windows\\System32")
    assert "local_dir contains unsafe path traversal" in str(exc_info.value)


def test_setup_search_request_validation():
    # Valid search setup
    req = SetupSearchRequest(
        search_id="SEARCH_2026_01",
        brief_notes="Notes",
        jd_content="JD text"
    )
    assert req.search_id == "SEARCH_2026_01"

    # Invalid search_id with path traversal
    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="../../../etc/shadow",
            brief_notes="Notes",
            jd_content="JD text"
        )
    assert "search_id must contain only alphanumeric" in str(exc_info.value)


def test_refine_request_validation():
    # Valid gem_id
    req = RefineRequest(gem_id="gem1", instruction="Improve clarity")
    assert req.gem_id == "gem1"

    # Invalid gem_id with path traversal
    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(gem_id="../gem1", instruction="Improve clarity")
    assert "gem_id must contain only alphanumeric" in str(exc_info.value)
