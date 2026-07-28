from fastapi.testclient import TestClient
from api import app

client = TestClient(app, raise_server_exceptions=False)

def test_pipeline_request_search_id_traversal():
    # Test path traversal characters in search_id
    payload = {
        "search_id": "../malicious",
        "local_dir": "runs/test/inputs"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text

def test_pipeline_request_candidate_id_traversal():
    # Test path traversal characters in candidate_id
    payload = {
        "search_id": "SEARCH-001",
        "candidate_id": "../../etc/passwd",
        "local_dir": "runs/test/inputs"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "candidate_id" in response.text

def test_pipeline_request_local_dir_traversal():
    # Test path traversal/absolute paths in local_dir
    payloads = [
        {"search_id": "SEARCH-001", "local_dir": "../../etc"},
        {"search_id": "SEARCH-001", "local_dir": "/etc/passwd"},
        {"search_id": "SEARCH-001", "local_dir": "C:\\Windows\\System32"},
    ]
    for p in payloads:
        response = client.post("/api/v1/run", json=p)
        assert response.status_code == 422
        assert "local_dir" in response.text

def test_setup_search_request_search_id_traversal():
    # Test path traversal in setup_search search_id
    payload = {
        "search_id": "nested/../../path",
        "brief_notes": "test brief",
        "jd_content": "test jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text

def test_refine_request_gem_id_traversal():
    # Test path traversal in refine gem_id
    payload = {
        "gem_id": "gem1/../../../etc",
        "instruction": "make it short"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "gem_id" in response.text

def test_valid_requests_pass_validation():
    # Test valid payload structure doesn't trigger 422 for input validation errors
    # Note: We won't fully run the pipeline since we don't have API keys / mock folders,
    # but we should get a 400 or other errors instead of Pydantic validation 422.
    payload = {
        "search_id": "SEARCH-TEST-001",
        "local_dir": "runs/SEARCH-TEST-001/inputs",
        "candidate_id": "candidate-001"
    }
    response = client.post("/api/v1/run", json=payload)
    # Since search_id and local_dir are valid formats, Pydantic should pass,
    # and the app will try to run the pipeline, returning 400 because GEMINI_API_KEY is not set or input dir doesn't exist
    assert response.status_code != 422
