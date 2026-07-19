import pytest
from fastapi.testclient import TestClient
import os

from api import app

# Use FastAPI TestClient with raise_server_exceptions=False to ensure validation errors
# return 422 Unprocessable Entity instead of raising exceptions or server errors.
client = TestClient(app, raise_server_exceptions=False)

def test_pipeline_request_path_traversal():
    """Verify that path traversal or invalid characters in PipelineRequest trigger a 422 Unprocessable Entity."""
    # Test path traversal in search_id
    payload = {
        "search_id": "../sensitive_dir",
        "local_dir": "runs/test"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text

    # Test path traversal in candidate_id
    payload2 = {
        "search_id": "valid-search-id",
        "local_dir": "runs/test",
        "candidate_id": "../../../etc/passwd"
    }
    response2 = client.post("/api/v1/run", json=payload2)
    assert response2.status_code == 422
    assert "candidate_id" in response2.text

    # Test valid inputs
    payload3 = {
        "search_id": "valid_search-123",
        "local_dir": "runs/test",
        "candidate_id": "candidate-99"
    }
    # Should get past input validation but fail on missing API Key or drive folder (raising 400 or another error but not 422 validation error)
    response3 = client.post("/api/v1/run", json=payload3)
    assert response3.status_code != 422


def test_setup_search_path_traversal():
    """Verify that path traversal in SetupSearchRequest triggers a 422 Unprocessable Entity."""
    payload = {
        "search_id": "sub_dir/../../exploit",
        "brief_notes": "test brief",
        "jd_content": "test jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text


def test_refine_gem_path_traversal():
    """Verify that path traversal in RefineRequest triggers a 422 Unprocessable Entity."""
    payload = {
        "gem_id": "gem1/../../../hack",
        "instruction": "refine something"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "gem_id" in response.text


def test_valid_id_patterns():
    """Verify that valid IDs containing alphanumeric, dashes, and underscores pass validation."""
    from pydantic import ValidationError
    from api import PipelineRequest

    # Should succeed validation
    req = PipelineRequest(
        search_id="valid-ID_123",
        local_dir="runs/test"
    )
    assert req.search_id == "valid-ID_123"

    # Should fail validation
    with pytest.raises(ValidationError):
        PipelineRequest(
            search_id="invalid/id",
            local_dir="runs/test"
        )
