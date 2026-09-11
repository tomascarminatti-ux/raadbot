import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH_001",
        candidate_id="CANDIDATE-02",
        local_dir="data/inputs",
    )
    assert req.search_id == "SEARCH_001"
    assert req.candidate_id == "CANDIDATE-02"
    assert req.local_dir == "data/inputs"


def test_pipeline_request_path_traversal_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../etc/passwd", local_dir="data/inputs")
    assert "Identificador inválido" in str(excinfo.value)


def test_pipeline_request_path_traversal_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="SEARCH_001", candidate_id="../../../secret")
    assert "Identificador inválido" in str(excinfo.value)


def test_pipeline_request_path_traversal_local_dir():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="SEARCH_001", local_dir="../secrets")
    assert "Ruta de directorio local inválida" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="SEARCH_001", local_dir="/etc/passwd")
    assert "Ruta de directorio local inválida" in str(excinfo.value)


def test_setup_search_request_validation():
    # Valid
    req = SetupSearchRequest(search_id="SEARCH_123", brief_notes="notes", jd_content="jd")
    assert req.search_id == "SEARCH_123"

    # Invalid search_id with path traversal
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(search_id="../../etc/passwd", brief_notes="notes", jd_content="jd")
    assert "search_id inválido" in str(excinfo.value)


def test_refine_request_validation():
    # Valid
    req = RefineRequest(gem_id="gem1", instruction="make concise")
    assert req.gem_id == "gem1"

    # Invalid gem_id with path traversal
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="../gem1", instruction="make concise")
    assert "gem_id inválido" in str(excinfo.value)
