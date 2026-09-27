import pytest
from fastapi.testclient import TestClient
from api import app, RefineRequest
from pydantic import ValidationError


def test_refine_request_valid_gem_id():
    req = RefineRequest(gem_id="gem1", instruction="Make concise")
    assert req.gem_id == "gem1"


def test_refine_request_path_traversal_rejected():
    invalid_ids = [
        "../config",
        "../../etc/passwd",
        "gem1/../../etc/passwd",
        "gem1.py",
        "gem1.md",
        "gem1/extra",
        "gem 1",
        "gem1\0",
    ]
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            RefineRequest(gem_id=invalid_id, instruction="Test instruction")


def test_refine_api_endpoint_invalid_gem_id():
    client = TestClient(app)
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../config", "instruction": "Test instruction"}
    )
    assert response.status_code == 422
