import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_path_traversal():
    """Verifica que PipelineRequest rechace entradas con path traversal o caracteres inválidos."""
    # Invalid search_id with path traversal
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../../etc", local_dir="data")
    assert "search_id" in str(exc_info.value) or "Identificador" in str(exc_info.value)

    # Invalid candidate_id with path traversal
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="search1", candidate_id="../candidate_x")
    assert "candidate_id" in str(exc_info.value) or "Identificador" in str(
        exc_info.value
    )

    # Invalid local_dir with path traversal
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="search1", local_dir="../inputs")
    assert "local_dir" in str(exc_info.value) or "Ruta" in str(exc_info.value)

    # Invalid absolute local_dir
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="search1", local_dir="/etc/passwd")
    assert "local_dir" in str(exc_info.value) or "Ruta" in str(exc_info.value)


def test_pipeline_request_valid_inputs():
    """Verifica que PipelineRequest acepte entradas válidas."""
    req = PipelineRequest(
        search_id="search-123_abc", candidate_id="cand_1", local_dir="inputs/search_123"
    )
    assert req.search_id == "search-123_abc"
    assert req.candidate_id == "cand_1"
    assert req.local_dir == "inputs/search_123"


def test_setup_search_request_path_traversal():
    """Verifica que SetupSearchRequest rechace search_id malicioso."""
    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../../../etc/passwd", brief_notes="notes", jd_content="jd"
        )


def test_refine_request_path_traversal():
    """Verifica que RefineRequest rechace gem_id con path traversal."""
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="refine prompt")
