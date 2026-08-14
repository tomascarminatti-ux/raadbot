import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    # Valid input should succeed
    req = PipelineRequest(
        search_id="valid-search-123_abc",
        candidate_id="valid-cand-456",
        local_dir="relative/path/to/dir",
    )
    assert req.search_id == "valid-search-123_abc"
    assert req.candidate_id == "valid-cand-456"
    assert req.local_dir == "relative/path/to/dir"


def test_pipeline_request_invalid_search_id():
    # Path traversal attempt in search_id should fail
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../invalid")
    assert "search_id" in str(excinfo.value)

    # Special characters in search_id should fail
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="invalid;id")
    assert "search_id" in str(excinfo.value)


def test_pipeline_request_invalid_candidate_id():
    # Path traversal attempt in candidate_id should fail
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_id", candidate_id="cand/../../etc")
    assert "candidate_id" in str(excinfo.value)


def test_pipeline_request_invalid_local_dir():
    # Absolute path should fail
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_id", local_dir="/etc/passwd")
    assert "local_dir" in str(excinfo.value)

    # Traversal sequence should fail
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_id", local_dir="some/path/../outside")
    assert "local_dir" in str(excinfo.value)

    # Windows drive letter should fail
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_id", local_dir="C:/Windows")
    assert "local_dir" in str(excinfo.value)


def test_setup_search_request():
    # Valid
    req = SetupSearchRequest(
        search_id="valid_setup", brief_notes="some notes", jd_content="some jd"
    )
    assert req.search_id == "valid_setup"

    # Invalid search_id with traversal
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="setup/../../etc",
            brief_notes="some notes",
            jd_content="some jd",
        )
    assert "search_id" in str(excinfo.value)


def test_refine_request():
    # Valid gem_id
    req = RefineRequest(gem_id="gem1", instruction="make it professional")
    assert req.gem_id == "gem1"

    # Invalid gem_id with special chars/traversal
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="gem1/../invalid", instruction="test")
    assert "gem_id" in str(excinfo.value)

    # Valid format but non-existent gem_id
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="gem99", instruction="test")
    assert "gem_id" in str(excinfo.value)
