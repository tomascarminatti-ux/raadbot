import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH_001",
        local_dir="inputs/search_1",
        candidate_id="CANDIDATE_123"
    )
    assert req.search_id == "SEARCH_001"
    assert req.local_dir == "inputs/search_1"
    assert req.candidate_id == "CANDIDATE_123"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../evil_path", local_dir="inputs/search_1")
    assert "search_id" in str(exc_info.value) or "Identificador inválido" in str(exc_info.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="SEARCH_1", candidate_id="cand; drop table;")
    assert "candidate_id" in str(exc_info.value) or "Identificador inválido" in str(exc_info.value)


def test_pipeline_request_path_traversal_local_dir():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="SEARCH_1", local_dir="../../../etc/passwd")
    assert "Ruta inválida" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="SEARCH_1", local_dir="/etc/passwd")
    assert "Ruta inválida" in str(exc_info.value)


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="SEARCH-123",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "SEARCH-123"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../search_123",
            brief_notes="notes",
            jd_content="jd"
        )


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="make it concise")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="hack")
