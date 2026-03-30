import os
import pytest
from fastapi.testclient import TestClient
from api import app

# Ensure GEMINI_API_KEY is set for startup check
os.environ["GEMINI_API_KEY"] = "dummy"

client = TestClient(app)

@pytest.mark.parametrize("endpoint,payload,field", [
    ("/api/v1/run", {"search_id": "../evil", "local_dir": "tests"}, "search_id"),
    ("/api/v1/run", {"search_id": "good", "local_dir": "/etc/passwd"}, "local_dir"),
    ("/api/v1/run", {"search_id": "good", "local_dir": "good", "candidate_id": "../evil"}, "candidate_id"),
    ("/api/v1/search/setup", {"search_id": "../evil", "brief_notes": "t", "jd_content": "t"}, "search_id"),
    ("/api/v1/gems/refine", {"gem_id": "../evil", "instruction": "t"}, "gem_id"),
])
def test_path_traversal_prevention(endpoint, payload, field):
    """Verify that path traversal attempts are blocked by Pydantic validation."""
    response = client.post(endpoint, json=payload)
    assert response.status_code == 422

    # Check if the error message mentions the pattern mismatch
    errors = response.json().get("detail", [])
    assert any(err.get("type") == "string_pattern_mismatch" and field in err.get("loc", []) for err in errors)

def test_valid_inputs_allowed():
    """Verify that valid IDs are still allowed."""
    # We use a non-existent gem_id so it fails later, but should pass Pydantic validation
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "valid-gem_123",
        "instruction": "test"
    })
    # Should not be a 422 (validation error)
    assert response.status_code != 422
