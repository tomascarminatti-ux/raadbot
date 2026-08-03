import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from api import app, PipelineRequest, SetupSearchRequest, RefineRequest

client = TestClient(app)

def test_pipeline_request_path_traversal_search_id():
    # Test path traversal in search_id via TestClient
    payload = {
        "search_id": "../etc/passwd",
        "local_dir": "runs/test"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Path traversal sequences are not allowed in identifiers" in response.text

def test_pipeline_request_path_traversal_candidate_id():
    # Test path traversal in candidate_id via TestClient
    payload = {
        "search_id": "clean-id",
        "local_dir": "runs/test",
        "candidate_id": "../../etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Path traversal sequences are not allowed in identifiers" in response.text

def test_pipeline_request_path_traversal_local_dir():
    # Test path traversal in local_dir via TestClient
    payload = {
        "search_id": "clean-id",
        "local_dir": "../../etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Directory traversal sequence '..' is not allowed" in response.text

def test_pipeline_request_absolute_path_local_dir():
    # Test absolute path rejection in local_dir via TestClient
    payload = {
        "search_id": "clean-id",
        "local_dir": "/etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "Absolute paths are not allowed" in response.text

def test_setup_search_path_traversal_search_id():
    # Test path traversal in SetupSearchRequest search_id via TestClient
    payload = {
        "search_id": "../malicious",
        "brief_notes": "test brief",
        "jd_content": "test jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "Path traversal sequences are not allowed in search_id" in response.text

def test_refine_gem_path_traversal_gem_id():
    # Test path traversal in RefineRequest gem_id via TestClient
    payload = {
        "gem_id": "../../etc/passwd",
        "instruction": "make it safer"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "Invalid gem_id" in response.text

def test_refine_gem_invalid_gem_id():
    # Test invalid gem_id which is not allowed via TestClient
    payload = {
        "gem_id": "invalid_gem",
        "instruction": "make it safer"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "Invalid gem_id" in response.text


# Direct Pydantic model validation tests

def test_pipeline_request_validation_direct():
    # Valid inputs should pass
    req = PipelineRequest(search_id="clean-id-123", local_dir="runs/test")
    assert req.search_id == "clean-id-123"
    assert req.local_dir == "runs/test"

    # Invalid search_id
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../invalid", local_dir="runs/test")
    assert "Path traversal sequences are not allowed in identifiers" in str(excinfo.value)

    # Invalid candidate_id
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="clean-id", local_dir="runs/test", candidate_id="c/../../a")
    assert "Path traversal sequences are not allowed in identifiers" in str(excinfo.value)

    # Invalid local_dir with traversal
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="clean-id", local_dir="runs/../test")
    assert "Directory traversal sequence '..' is not allowed" in str(excinfo.value)

    # Invalid local_dir with absolute path
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="clean-id", local_dir="/etc")
    assert "Absolute paths are not allowed" in str(excinfo.value)


def test_setup_search_request_validation_direct():
    # Valid search_id should pass
    req = SetupSearchRequest(search_id="clean-search-id", brief_notes="...", jd_content="...")
    assert req.search_id == "clean-search-id"

    # Invalid search_id with traversal
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(search_id="search/../id", brief_notes="...", jd_content="...")
    assert "Path traversal sequences are not allowed in search_id" in str(excinfo.value)


def test_refine_request_validation_direct():
    # Valid gem_id should pass
    req = RefineRequest(gem_id="gem1", instruction="...")
    assert req.gem_id == "gem1"

    # Invalid gem_id should fail
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="invalid_gem", instruction="...")
    assert "Invalid gem_id" in str(excinfo.value)
