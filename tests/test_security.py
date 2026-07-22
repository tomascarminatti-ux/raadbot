import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app, raise_server_exceptions=False)

def test_pipeline_request_search_id_traversal():
    # Test path traversal in search_id
    response = client.post("/api/v1/run", json={
        "search_id": "../malicious",
        "drive_folder": "some_folder"
    })
    assert response.status_code == 422
    assert "search_id" in response.text

def test_pipeline_request_candidate_id_traversal():
    # Test path traversal in candidate_id
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id",
        "drive_folder": "some_folder",
        "candidate_id": "../../bad"
    })
    assert response.status_code == 422
    assert "candidate_id" in response.text

def test_setup_search_request_search_id_traversal():
    # Test path traversal in SetupSearchRequest.search_id
    response = client.post("/api/v1/search/setup", json={
        "search_id": "runs/../../traversal",
        "brief_notes": "notes",
        "jd_content": "jd"
    })
    assert response.status_code == 422
    assert "search_id" in response.text

def test_refine_request_gem_id_traversal():
    # Test path traversal in RefineRequest.gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../../gem1",
        "instruction": "refine it"
    })
    assert response.status_code == 422
    assert "gem_id" in response.text

def test_valid_requests():
    # Test valid requests do not fail Pydantic validation
    from api import PipelineRequest, SetupSearchRequest, RefineRequest

    # This should pass without raising ValidationError
    req = PipelineRequest(search_id="valid_search-123", candidate_id="cand_12-A")
    assert req.search_id == "valid_search-123"
    assert req.candidate_id == "cand_12-A"

    req2 = SetupSearchRequest(search_id="some-id", brief_notes="notes", jd_content="content")
    assert req2.search_id == "some-id"

    req3 = RefineRequest(gem_id="gem1", instruction="make it better")
    assert req3.gem_id == "gem1"
