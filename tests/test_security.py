import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_pipeline_request_path_traversal_validation():
    # Test path traversal in search_id
    payload = {
        "search_id": "../etc/passwd",
        "local_dir": "valid_dir"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Identifier must contain only alphanumeric" in response.text

    # Test path traversal in candidate_id
    payload = {
        "search_id": "valid_search_id",
        "candidate_id": "../../../secret",
        "local_dir": "valid_dir"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Identifier must contain only alphanumeric" in response.text

    # Test path traversal in local_dir
    payload = {
        "search_id": "valid_search_id",
        "local_dir": "../relative/path"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Path traversal vectors or absolute paths are prohibited" in response.text

    # Test absolute path in local_dir
    payload = {
        "search_id": "valid_search_id",
        "local_dir": "/etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Path traversal vectors or absolute paths are prohibited" in response.text


def test_setup_search_request_path_traversal_validation():
    payload = {
        "search_id": "../invalid_search_id",
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "Identifier must contain only alphanumeric" in response.text


def test_refine_request_path_traversal_validation():
    payload = {
        "gem_id": "../gem1",
        "instruction": "refine prompt"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "Identifier must contain only alphanumeric" in response.text


def test_valid_identifiers_allowed():
    from api import PipelineRequest, SetupSearchRequest, RefineRequest

    req1 = PipelineRequest(search_id="valid_search-123", candidate_id="candidate_01", local_dir="inputs/search1")
    assert req1.search_id == "valid_search-123"
    assert req1.candidate_id == "candidate_01"
    assert req1.local_dir == "inputs/search1"

    req2 = SetupSearchRequest(search_id="valid_search_id", brief_notes="notes", jd_content="jd")
    assert req2.search_id == "valid_search_id"

    req3 = RefineRequest(gem_id="gem1", instruction="make it shorter")
    assert req3.gem_id == "gem1"
