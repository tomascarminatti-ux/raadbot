import sys
import os
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app

client = TestClient(app)


@pytest.mark.parametrize(
    "invalid_search_id",
    [
        "../malicious",
        "../../etc",
        "search/../../id",
        "search id",
        "search_id_with_special_#@!",
        "/absolute/path",
    ],
)
def test_pipeline_request_invalid_search_id(invalid_search_id):
    """Verify that PipelineRequest rejects invalid search_id with 422 status."""
    payload = {"search_id": invalid_search_id, "local_dir": "valid_dir"}
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text or "Identifier" in response.text


@pytest.mark.parametrize(
    "invalid_candidate_id",
    [
        "../malicious",
        "../../etc",
        "candidate/../../id",
        "candidate id",
        "candidate#1",
    ],
)
def test_pipeline_request_invalid_candidate_id(invalid_candidate_id):
    """Verify that PipelineRequest rejects invalid candidate_id with 422 status."""
    payload = {
        "search_id": "valid-search-123",
        "candidate_id": invalid_candidate_id,
        "local_dir": "valid_dir",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "candidate_id" in response.text or "Identifier" in response.text


@pytest.mark.parametrize(
    "invalid_local_dir",
    [
        "../malicious",
        "../../etc",
        "dir/../../etc",
        "/absolute/path",
        "C:\\windows",
    ],
)
def test_pipeline_request_invalid_local_dir(invalid_local_dir):
    """Verify that PipelineRequest rejects invalid local_dir with 422 status."""
    payload = {"search_id": "valid-search-123", "local_dir": invalid_local_dir}
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "local_dir" in response.text


@pytest.mark.parametrize(
    "invalid_search_id",
    [
        "../malicious",
        "../../etc",
        "search/../../id",
        "/absolute/path",
    ],
)
def test_setup_search_invalid_search_id(invalid_search_id):
    """Verify that SetupSearchRequest rejects invalid search_id with 422 status."""
    payload = {
        "search_id": invalid_search_id,
        "brief_notes": "notes",
        "jd_content": "jd",
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "invalid_gem_id",
    [
        "../malicious",
        "../../etc",
        "gem/../../id",
        "/absolute/path",
    ],
)
def test_refine_gem_invalid_gem_id(invalid_gem_id):
    """Verify that RefineRequest rejects invalid gem_id with 422 status."""
    payload = {"gem_id": invalid_gem_id, "instruction": "refine it"}
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422


@patch("api.run_pipeline", new_callable=AsyncMock)
def test_pipeline_request_valid_inputs(mock_run_pipeline):
    """Verify that valid inputs pass validation and invoke processing."""
    mock_run_pipeline.return_value = {
        "status": "success",
        "search_id": "valid_search-123",
        "output_dir": "runs/valid_search-123/outputs",
        "summary": {},
    }
    payload = {
        "search_id": "valid_search-123",
        "local_dir": "valid_relative_dir/nested",
        "candidate_id": "valid_candidate-456",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 200
    mock_run_pipeline.assert_called_once()
