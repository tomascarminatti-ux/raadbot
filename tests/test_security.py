import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_valid_request_models():
    """Verifica que inputs válidos pasen la validación Pydantic."""
    req = PipelineRequest(search_id="valid_search-123", candidate_id="cand_1", local_dir="inputs/folder")
    assert req.search_id == "valid_search-123"
    assert req.candidate_id == "cand_1"
    assert req.local_dir == "inputs/folder"

    setup_req = SetupSearchRequest(search_id="search_1", brief_notes="notes", jd_content="jd")
    assert setup_req.search_id == "search_1"

    refine_req = RefineRequest(gem_id="gem1", instruction="refine this")
    assert refine_req.gem_id == "gem1"


def test_invalid_search_id_path_traversal():
    """Verifica que intentos de path traversal en search_id sean rechazados."""
    invalid_ids = ["../evil", "../../etc/passwd", "search/123", "search\\123", "search_id; drop table"]
    for bad_id in invalid_ids:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id=bad_id)

        with pytest.raises(ValidationError):
            SetupSearchRequest(search_id=bad_id, brief_notes="notes", jd_content="jd")


def test_invalid_candidate_id():
    """Verifica que candidate_id con caracteres inválidos sea rechazado."""
    invalid_candidates = ["../cand", "cand/1", "cand\\1"]
    for bad_cand in invalid_candidates:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="valid_search", candidate_id=bad_cand)


def test_invalid_local_dir_path_traversal():
    """Verifica que local_dir rechace directory traversal o rutas absolutas."""
    invalid_paths = ["../secret", "folder/../../etc", "/etc/passwd", "C:\\Windows\\System32"]
    for bad_path in invalid_paths:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="valid_search", local_dir=bad_path)


def test_invalid_gem_id():
    """Verifica que gem_id con path traversal o caracteres inválidos sea rechazado."""
    invalid_gems = ["../gem1", "gem1/2", "gem1\\2", "../../api"]
    for bad_gem in invalid_gems:
        with pytest.raises(ValidationError):
            RefineRequest(gem_id=bad_gem, instruction="test")
