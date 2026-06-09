
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api import app
import config

client = TestClient(app)

@pytest.mark.parametrize("endpoint,payload", [
    ("/api/v1/run", {"search_id": "../traversal", "local_dir": "."}),
    ("/api/v1/run", {"search_id": "valid", "candidate_id": "sub/dir", "local_dir": "."}),
    ("/api/v1/search/setup", {"search_id": "path/traversal", "brief_notes": "x", "jd_content": "y"}),
    ("/api/v1/gems/refine", {"gem_id": "not_a_gem", "instruction": "x"}),
    ("/api/v1/gems/refine", {"gem_id": "../outside", "instruction": "x"}),
    ("/api/v1/gems/refine", {"gem_id": "gem1;rm -rf /", "instruction": "x"}),
])
def test_identifier_validation_blocks_bad_input(endpoint, payload):
    response = client.post(endpoint, json=payload)
    # Pydantic validation error is 422
    # gem_id validation in code is 403 or 404 (if it matches pattern but not whitelist)
    assert response.status_code in [422, 403]

def test_gem_id_whitelist():
    # Matches pattern but not in config.ALLOWED_GEMS
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "unknown_gem",
        "instruction": "test"
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Access to this GEM is restricted"

def test_valid_identifiers_accepted():
    # We use /api/v1/gems/refine which we know exists for 'gem1'

    with patch("api.GeminiClient.run_gem") as mock_run:
        mock_run.return_value = {"markdown": "new prompt", "raw": "new prompt"}

        response = client.post("/api/v1/gems/refine", json={
            "gem_id": "gem1", # valid and in whitelist
            "instruction": "test"
        })

        # Should not be 422 (pydantic) or 403 (whitelist)
        assert response.status_code not in [422, 403]
        # Since 'gem1' exists in prompts/, it should succeed if mocked
        assert response.status_code == 200
