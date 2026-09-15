import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest

def test_pipeline_request_valid_identifiers():
    req = PipelineRequest(search_id="search_123-abc", candidate_id="candidate_456")
    assert req.search_id == "search_123-abc"
    assert req.candidate_id == "candidate_456"

def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search/../123")
    assert "Identifier must contain only alphanumeric characters, dashes, or underscores." in str(excinfo.value)

def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", candidate_id="cand; rm -rf /")
    assert "Identifier must contain only alphanumeric characters, dashes, or underscores." in str(excinfo.value)

def test_pipeline_request_valid_local_dir():
    req = PipelineRequest(search_id="search1", local_dir="data/inputs/search1")
    assert req.local_dir == "data/inputs/search1"

def test_pipeline_request_path_traversal_local_dir():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", local_dir="../etc/passwd")
    assert "local_dir cannot contain path traversal or absolute path references." in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", local_dir="data/../../secret")
    assert "local_dir cannot contain path traversal or absolute path references." in str(excinfo.value)

def test_pipeline_request_absolute_path_local_dir():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", local_dir="/etc/passwd")
    assert "local_dir cannot contain path traversal or absolute path references." in str(excinfo.value)

def test_setup_search_request_validation():
    # Valid
    req = SetupSearchRequest(search_id="search-01", brief_notes="notes", jd_content="jd")
    assert req.search_id == "search-01"

    # Invalid
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(search_id="search/1", brief_notes="notes", jd_content="jd")
    assert "search_id must contain only alphanumeric characters, dashes, or underscores." in str(excinfo.value)

def test_refine_request_validation():
    # Valid
    req = RefineRequest(gem_id="gem1", instruction="Improve clarity")
    assert req.gem_id == "gem1"

    # Invalid path traversal attempt
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="../config", instruction="Malicious")
    assert "gem_id must contain only alphanumeric characters, dashes, or underscores." in str(excinfo.value)
