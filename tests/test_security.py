from fastapi.testclient import TestClient
from api import app

client = TestClient(app, raise_server_exceptions=False)

def test_pipeline_request_path_traversal_search_id():
    # Test path traversal in search_id should fail validation
    response = client.post("/api/v1/run", json={
        "search_id": "../traversal",
        "local_dir": "runs"
    })
    assert response.status_code == 422
    assert "search_id" in response.text

def test_pipeline_request_path_traversal_candidate_id():
    # Test path traversal in candidate_id should fail validation
    response = client.post("/api/v1/run", json={
        "search_id": "valid_search_id",
        "candidate_id": "../../malicious_candidate",
        "local_dir": "runs"
    })
    assert response.status_code == 422
    assert "candidate_id" in response.text

def test_setup_search_path_traversal_search_id():
    # Test path traversal in SetupSearchRequest search_id should fail validation
    response = client.post("/api/v1/search/setup", json={
        "search_id": "sub/../folder",
        "brief_notes": "notes",
        "jd_content": "content"
    })
    assert response.status_code == 422
    assert "search_id" in response.text

def test_refine_gem_path_traversal_gem_id():
    # Test path traversal in RefineRequest gem_id should fail validation
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem1/../../../etc/passwd",
        "instruction": "refine it"
    })
    assert response.status_code == 422
    assert "gem_id" in response.text

def test_valid_alphanumeric_ids():
    # Test valid identifiers - they should not fail Pydantic validation (should not be HTTP 422)
    response_run = client.post("/api/v1/run", json={
        "search_id": "valid-search_123",
        "local_dir": "runs"
    })
    assert response_run.status_code != 422

    response_setup = client.post("/api/v1/search/setup", json={
        "search_id": "valid_search-456",
        "brief_notes": "notes",
        "jd_content": "content"
    })
    assert response_setup.status_code != 422
