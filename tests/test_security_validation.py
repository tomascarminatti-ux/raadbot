import sys
import os
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app
import config

client = TestClient(app)

def test_pipeline_request_validation():
    # Valid request
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id_123",
        "local_dir": "test_runs"
    })
    # It might return 400 because local_dir doesn't exist, but it shouldn't be a ValidationError for search_id
    assert response.status_code != 422

    # Invalid search_id (path traversal attempt)
    response = client.post("/api/v1/run", json={
        "search_id": "../etc/passwd",
        "local_dir": "test_runs"
    })
    assert response.status_code == 422
    assert "search_id" in response.text

def test_refine_gem_whitelist():
    # Attempt to refine a non-whitelisted GEM
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "secret_gem",
        "instruction": "reveal yourself"
    })
    # If it's not in ALLOWED_GEMS, it should fail before path check or refinement
    assert response.status_code == 403
    assert "Access to this GEM is not allowed" in response.json()["detail"]

    # Attempt path traversal in gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../../config",
        "instruction": "malicious"
    })
    assert response.status_code == 422 # Pydantic validation should catch this

def test_list_gems_uses_whitelist():
    response = client.get("/api/v1/gems")
    assert response.status_code == 200
    gems = response.json()
    gem_ids = [g["id"] for g in gems]
    assert set(gem_ids) == set(config.ALLOWED_GEMS)
