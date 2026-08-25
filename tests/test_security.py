import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        candidate_id="cand_456",
        local_dir="inputs/valid_dir"
    )
    assert req.search_id == "search_123"
    assert req.candidate_id == "cand_456"
    assert req.local_dir == "inputs/valid_dir"


def test_pipeline_request_path_traversal_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../invalid_search", local_dir="inputs/valid_dir")
    assert "Identificador inválido" in str(excinfo.value)


def test_pipeline_request_path_traversal_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="valid_search",
            candidate_id="../../etc/passwd",
            local_dir="inputs/valid_dir"
        )
    assert "Identificador inválido" in str(excinfo.value)


def test_pipeline_request_path_traversal_local_dir():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", local_dir="inputs/../etc/passwd")
    assert "Ruta de directorio no permitida" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid_search", local_dir="/etc/passwd")
    assert "Ruta de directorio no permitida" in str(excinfo.value)


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="valid-search-1",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "valid-search-1"

    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="../invalid/path",
            brief_notes="notes",
            jd_content="jd"
        )
    assert "search_id inválido" in str(excinfo.value)


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="make it better")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="gem1/../../secret", instruction="make it better")
    assert "gem_id inválido" in str(excinfo.value)
