import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api import PipelineRequest, RefineRequest, SetupSearchRequest, app

client = TestClient(app)


def test_pipeline_request_validators():
    # Valid model instantiation
    req = PipelineRequest(
        search_id="valid_search-123",
        local_dir="runs/valid_search-123/inputs",
        candidate_id="valid-candidate_456",
    )
    assert req.search_id == "valid_search-123"
    assert req.local_dir == "runs/valid_search-123/inputs"
    assert req.candidate_id == "valid-candidate_456"

    # Test invalid search_id with special characters
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="invalid/search", local_dir="inputs")
    assert "search_id" in str(excinfo.value)

    # Test invalid candidate_id with path traversal characters
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid", candidate_id="../traversal")
    assert "candidate_id" in str(excinfo.value)

    # Test local_dir with backslashes normalization
    req_backslashes = PipelineRequest(search_id="valid", local_dir="runs\\test\\inputs")
    assert req_backslashes.local_dir == "runs/test/inputs"

    # Test local_dir with path traversal sequence
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid", local_dir="runs/../../etc/passwd")
    assert "Directory traversal sequence" in str(excinfo.value)

    # Test local_dir with backslash-based traversal sequence
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid", local_dir="runs/..\\..\\etc/passwd")
    assert "Directory traversal sequence" in str(excinfo.value)

    # Test local_dir with absolute path
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid", local_dir="/etc/passwd")
    assert "Absolute paths are not allowed" in str(excinfo.value)


def test_setup_search_request_validators():
    # Valid
    req = SetupSearchRequest(search_id="valid-1", brief_notes="notes", jd_content="jd")
    assert req.search_id == "valid-1"

    # Invalid search_id
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(search_id="invalid;id", brief_notes="notes", jd_content="jd")
    assert "search_id" in str(excinfo.value)


def test_refine_request_validators():
    # Valid
    req = RefineRequest(gem_id="gem1", instruction="add details")
    assert req.gem_id == "gem1"

    # Invalid gem_id
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="gem..1", instruction="add details")
    assert "gem_id" in str(excinfo.value)


def test_api_endpoints_rejection_of_path_traversal():
    # 1. Pipeline trigger validation
    response = client.post(
        "/api/v1/run", json={"search_id": "bad/id", "local_dir": "runs/test"}
    )
    assert response.status_code == 422
    assert "search_id" in response.text

    response = client.post(
        "/api/v1/run", json={"search_id": "valid", "local_dir": "runs/../../etc"}
    )
    assert response.status_code == 422
    assert "Directory traversal" in response.text

    # 2. Setup search validation
    response = client.post(
        "/api/v1/search/setup",
        json={"search_id": "bad/id", "brief_notes": "notes", "jd_content": "jd"},
    )
    assert response.status_code == 422
    assert "search_id" in response.text

    # 3. Refine gem validation
    response = client.post(
        "/api/v1/gems/refine", json={"gem_id": "bad/id", "instruction": "refine"}
    )
    assert response.status_code == 422
    assert "gem_id" in response.text
