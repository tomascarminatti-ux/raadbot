import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient

from api import app, PipelineRequest, SetupSearchRequest, RefineRequest

client = TestClient(app)


def test_valid_pipeline_request():
    req = PipelineRequest(
        search_id="search-123_abc",
        candidate_id="candidate_001",
        local_dir="data/inputs",
    )
    assert req.search_id == "search-123_abc"
    assert req.candidate_id == "candidate_001"
    assert req.local_dir == "data/inputs"


def test_invalid_search_id_path_traversal():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../invalid_id")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search/../../etc/passwd")

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../etc",
            brief_notes="test",
            jd_content="test",
        )


def test_invalid_gem_id_path_traversal():
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="test")

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem1/../../secret", instruction="test")


def test_invalid_local_dir_path_traversal():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="../secret_dir")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="/etc/passwd")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="C:\\Windows\\System32")


def test_api_endpoints_reject_path_traversal():
    # Test POST /api/v1/run
    response = client.post(
        "/api/v1/run",
        json={"search_id": "../traversal", "local_dir": "data/inputs"},
    )
    assert response.status_code == 422

    # Test POST /api/v1/search/setup
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../../runs/bad",
            "brief_notes": "notes",
            "jd_content": "jd",
        },
    )
    assert response.status_code == 422

    # Test POST /api/v1/gems/refine
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../gem1", "instruction": "malicious instruction"},
    )
    assert response.status_code == 422
