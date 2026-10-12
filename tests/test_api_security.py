import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_refine_request_valid_gem_id():
    req = RefineRequest(gem_id="gem1", instruction="Improve clarity")
    assert req.gem_id == "gem1"


def test_refine_request_path_traversal_rejected():
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="../gem1", instruction="Attack")
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="gem1/../gem2", instruction="Attack")
    assert "Identifier must contain only alphanumeric characters" in str(excinfo.value)


def test_pipeline_request_valid():
    req = PipelineRequest(search_id="search_123", candidate_id="cand_1", local_dir="inputs/test")
    assert req.search_id == "search_123"
    assert req.candidate_id == "cand_1"
    assert req.local_dir == "inputs/test"


def test_pipeline_request_path_traversal_rejected():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../../etc/passwd")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", candidate_id="../cand")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="../secret_dir")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="/absolute/path")


def test_setup_search_request_validation():
    req = SetupSearchRequest(search_id="valid_search", brief_notes="notes", jd_content="jd")
    assert req.search_id == "valid_search"

    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="search/../id", brief_notes="notes", jd_content="jd")
