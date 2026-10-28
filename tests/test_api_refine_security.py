import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from api import app, RefineRequest

client = TestClient(app)

def test_refine_request_valid_gem_id():
    req = RefineRequest(gem_id="gem1", instruction="Improve clarity")
    assert req.gem_id == "gem1"
    assert req.instruction == "Improve clarity"

def test_refine_request_invalid_gem_id_path_traversal():
    invalid_ids = [
        "../gem1",
        "..\\gem1",
        "gem1/../../etc/passwd",
        "gem1\x00",
        "gem1.md",
        "gem1; id",
        "gem 1",
    ]
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            RefineRequest(gem_id=invalid_id, instruction="Test instruction")

def test_refine_endpoint_rejects_path_traversal():
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../gem1", "instruction": "Test instruction"},
    )
    assert response.status_code == 422
