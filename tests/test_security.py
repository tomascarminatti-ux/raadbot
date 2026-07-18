import pytest
from fastapi.testclient import TestClient
from api import app, PipelineRequest, SetupSearchRequest, RefineRequest
from pydantic import ValidationError

client = TestClient(app, raise_server_exceptions=False)

def test_pydantic_models_validation_invalid():
    # Test PipelineRequest with invalid search_id
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../traversal", local_dir="some_dir")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", candidate_id="cand/../../traversal")

    # Test SetupSearchRequest with invalid search_id
    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="bad/path",
            brief_notes="some notes",
            jd_content="some jd"
        )

    # Test RefineRequest with invalid gem_id
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem/..", instruction="refine")

def test_pydantic_models_validation_valid():
    # Verify valid values work without raising validation errors
    req = PipelineRequest(search_id="valid_search-123", candidate_id="cand_123")
    assert req.search_id == "valid_search-123"
    assert req.candidate_id == "cand_123"

    req2 = SetupSearchRequest(search_id="search_1", brief_notes="notes", jd_content="jd")
    assert req2.search_id == "search_1"

    req3 = RefineRequest(gem_id="gem1", instruction="refine")
    assert req3.gem_id == "gem1"

def test_api_endpoints_path_traversal_returns_422():
    # Test triggering pipeline with malicious path traversal search_id
    response = client.post("/api/v1/run", json={
        "search_id": "runs/../../traversal",
        "local_dir": "runs"
    })
    assert response.status_code == 422

    # Test setup search with malicious search_id
    response = client.post("/api/v1/search/setup", json={
        "search_id": "../malicious",
        "brief_notes": "notes",
        "jd_content": "jd"
    })
    assert response.status_code == 422

    # Test refine gem with malicious gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "prompts/../../etc/passwd",
        "instruction": "refine"
    })
    assert response.status_code == 422
