from fastapi.testclient import TestClient
import os
import pytest
from api import app, RefineRequest

# Set dummy API key to pass startup check if needed
os.environ["GEMINI_API_KEY"] = "dummy"

client = TestClient(app)

@pytest.mark.parametrize("gem_id", [
    "../../etc/passwd",
    "gem1/../../etc/passwd",
    "invalid_gem",
    "gem6",  # Only gem1-5 allowed
])
def test_refine_traversal_blocked(gem_id):
    payload = {
        "gem_id": gem_id,
        "instruction": "test"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422

@pytest.mark.parametrize("gem_id", ["gem1", "gem2", "gem3", "gem4", "gem5"])
def test_refine_valid_gem_allowed(gem_id):
    # Just check that it passes Pydantic validation
    req = RefineRequest(gem_id=gem_id, instruction="test")
    assert req.gem_id == gem_id

@pytest.mark.parametrize("search_id", [
    "../traversal",
    "search/../../secret",
    "search id with spaces",
    "search;id",
])
def test_pipeline_request_traversal_blocked(search_id):
    payload = {
        "search_id": search_id,
        "local_dir": "test_data"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_pipeline_request_valid_allowed():
    payload = {
        "search_id": "VALID-search_123",
        "local_dir": "test_data"
    }
    response = client.post("/api/v1/run", json=payload)
    # It might fail with 400 because test_data doesn't exist, but NOT 422
    assert response.status_code != 422
