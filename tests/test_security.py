import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient

from api import app, PipelineRequest, SetupSearchRequest, RefineRequest

client = TestClient(app)


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="inputs/search_123",
        candidate_id="cand-001"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "inputs/search_123"
    assert req.candidate_id == "cand-001"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../../etc/passwd", local_dir="inputs")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search/123", local_dir="inputs")


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search_123", candidate_id="../cand1")


def test_pipeline_request_invalid_local_dir():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search_123", local_dir="../secret_dir")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search_123", local_dir="/etc/passwd")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search_123", local_dir="C:\\Windows\\System32")


def test_setup_search_request_invalid_search_id():
    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../bad_id",
            brief_notes="notes",
            jd_content="jd"
        )


def test_refine_request_invalid_gem_id():
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="make it concise")


def test_refine_endpoint_path_traversal_rejection():
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../../config", "instruction": "malicious"}
    )
    assert response.status_code == 422
