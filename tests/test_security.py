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


@pytest.mark.parametrize(
    "bad_search_id",
    [
        "../traversal",
        "../../etc/passwd",
        "search id space",
        "search_id\n",
        "search/id",
        "search..id",
    ],
)
def test_pipeline_request_invalid_search_id(bad_search_id):
    with pytest.raises(ValidationError):
        PipelineRequest(search_id=bad_search_id, local_dir="inputs/test")


@pytest.mark.parametrize(
    "bad_local_dir",
    [
        "../inputs",
        "inputs/../../etc/passwd",
        "/absolute/path/to/dir",
        "C:\\Windows\\System32",
    ],
)
def test_pipeline_request_invalid_local_dir(bad_local_dir):
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir=bad_local_dir)


@pytest.mark.parametrize(
    "bad_candidate_id",
    [
        "../cand",
        "cand/01",
        "cand 01",
        "cand_id\n",
    ],
)
def test_pipeline_request_invalid_candidate_id(bad_candidate_id):
    with pytest.raises(ValidationError):
        PipelineRequest(
            search_id="valid_id",
            local_dir="inputs/valid",
            candidate_id=bad_candidate_id,
        )


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="valid-search_99",
        brief_notes="notes",
        jd_content="jd",
    )
    assert req.search_id == "valid-search_99"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../invalid_id",
            brief_notes="notes",
            jd_content="jd",
        )


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="refine this")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="refine this")


def test_api_endpoint_rejects_path_traversal():
    response = client.post(
        "/api/v1/run",
        json={"search_id": "../etc/passwd", "local_dir": "data/test"},
    )
    assert response.status_code == 422
