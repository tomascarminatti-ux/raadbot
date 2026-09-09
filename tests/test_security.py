import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest

def test_valid_requests():
    """Verifica que solicitudes válidas con identificadores y rutas limpias pasen la validación."""
    p_req = PipelineRequest(
        search_id="search_123",
        local_dir="data/inputs",
        candidate_id="candidate-abc_1"
    )
    assert p_req.search_id == "search_123"
    assert p_req.local_dir == "data/inputs"
    assert p_req.candidate_id == "candidate-abc_1"

    s_req = SetupSearchRequest(
        search_id="valid-search-99",
        brief_notes="notes",
        jd_content="jd content"
    )
    assert s_req.search_id == "valid-search-99"

    r_req = RefineRequest(
        gem_id="gem1",
        instruction="make it shorter"
    )
    assert r_req.gem_id == "gem1"

def test_path_traversal_identifiers():
    """Verifica que intentos de path traversal en identificadores lancen ValidationError."""
    invalid_ids = [
        "../etc/passwd",
        "../../secret",
        "gem1/../../etc",
        "search id with space",
        "search;id",
        "search$id",
        "search_id\n"
    ]

    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id=invalid_id)

        with pytest.raises(ValidationError):
            PipelineRequest(search_id="valid", candidate_id=invalid_id)

        with pytest.raises(ValidationError):
            SetupSearchRequest(search_id=invalid_id, brief_notes="a", jd_content="b")

        with pytest.raises(ValidationError):
            RefineRequest(gem_id=invalid_id, instruction="a")

def test_path_traversal_local_dir():
    """Verifica que intentos de directory traversal o rutas absolutas en local_dir lancen ValidationError."""
    invalid_paths = [
        "../data",
        "../../etc/passwd",
        "/etc/passwd",
        "C:\\Windows\\System32",
        "data/../../secret"
    ]

    for invalid_path in invalid_paths:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="valid_search", local_dir=invalid_path)
