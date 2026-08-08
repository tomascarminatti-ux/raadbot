import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api import app, PipelineRequest, SetupSearchRequest, RefineRequest

client = TestClient(app)


def test_pipeline_request_validation_valid():
    # Valid model fields
    req = PipelineRequest(
        search_id="valid-id_123",
        candidate_id="cand-id_9",
        local_dir="runs/valid_dir/path",
        drive_folder="drive_id",
    )
    assert req.search_id == "valid-id_123"
    assert req.candidate_id == "cand-id_9"
    assert req.local_dir == "runs/valid_dir/path"


def test_pipeline_request_validation_invalid_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search/id")
    assert "search_id" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search;injection")
    assert "search_id" in str(excinfo.value)


def test_pipeline_request_validation_invalid_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid", candidate_id="cand/id")
    assert "candidate_id" in str(excinfo.value)


def test_pipeline_request_validation_invalid_local_dir_traversal():
    # Simple traversal
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid", local_dir="runs/../../etc")
    assert "Directory traversal attempt" in str(excinfo.value)

    # Backslash traversal
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid", local_dir="runs\\..\\..\\etc")
    assert "Directory traversal attempt" in str(excinfo.value)


def test_pipeline_request_validation_invalid_local_dir_absolute():
    # Absolute path starting with /
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid", local_dir="/etc/passwd")
    assert "Absolute paths are not allowed" in str(excinfo.value)


def test_pipeline_request_validation_invalid_local_dir_drive():
    # Windows drive letters
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="valid", local_dir="C:/etc/passwd")
    assert "Drive letters are not allowed" in str(excinfo.value)


def test_setup_search_request_validation():
    # Valid
    req = SetupSearchRequest(
        search_id="valid-id",
        brief_notes="some brief notes",
        jd_content="some job description",
    )
    assert req.search_id == "valid-id"

    # Invalid search_id
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="invalid/id", brief_notes="some notes", jd_content="some jd"
        )
    assert "search_id" in str(excinfo.value)


def test_refine_request_validation():
    # Valid
    req = RefineRequest(gem_id="gem1", instruction="make it more detailed")
    assert req.gem_id == "gem1"

    # Invalid gem_id
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="gem1/../../etc", instruction="make it more detailed")
    assert "gem_id" in str(excinfo.value)


def test_fastapi_endpoints_reject_invalid_inputs():
    # Test triggering pipeline with invalid search_id
    response = client.post(
        "/api/v1/run", json={"search_id": "invalid/id", "local_dir": "runs/test"}
    )
    assert response.status_code == 422
    assert "search_id" in response.text

    # Test triggering pipeline with invalid local_dir
    response = client.post(
        "/api/v1/run", json={"search_id": "valid_id", "local_dir": "../invalid_dir"}
    )
    assert response.status_code == 422
    assert "Directory traversal attempt" in response.text

    # Test setup search with invalid search_id
    response = client.post(
        "/api/v1/search/setup",
        json={"search_id": "invalid/id", "brief_notes": "notes", "jd_content": "jd"},
    )
    assert response.status_code == 422
    assert "search_id" in response.text

    # Test refining gem with invalid gem_id
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "invalid/gem_id", "instruction": "refine"},
    )
    assert response.status_code == 422
    assert "gem_id" in response.text
