import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest

def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="data/search_123",
        candidate_id="cand_1"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "data/search_123"
    assert req.candidate_id == "cand_1"

def test_pipeline_request_invalid_search_id_path_traversal():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="../etc/passwd",
            local_dir="data/search_123"
        )
    assert "Identificador inválido" in str(excinfo.value)

def test_pipeline_request_invalid_candidate_id_path_traversal():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="search_123",
            candidate_id="../../etc/passwd",
            local_dir="data/search_123"
        )
    assert "Identificador inválido" in str(excinfo.value)

def test_pipeline_request_invalid_local_dir_traversal():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="search_123",
            local_dir="../secret_dir"
        )
    assert "Acceso a directorio inválido" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="search_123",
            local_dir="/etc/passwd"
        )
    assert "Acceso a directorio inválido" in str(excinfo.value)

def test_setup_search_request_invalid_search_id():
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="search/../123",
            brief_notes="notes",
            jd_content="jd"
        )
    assert "Identificador inválido" in str(excinfo.value)

def test_refine_request_invalid_gem_id():
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(
            gem_id="../../etc/passwd",
            instruction="refine prompt"
        )
    assert "Identificador de GEM inválido" in str(excinfo.value)
