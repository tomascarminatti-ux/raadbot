from fastapi.testclient import TestClient
from api import app
import pytest

client = TestClient(app)

def test_path_traversal_search_id():
    payload = {
        "search_id": "../../tmp/malicious",
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text

def test_path_traversal_local_dir():
    payload = {
        "search_id": "valid-id",
        "local_dir": "/etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "local_dir" in response.text

def test_path_traversal_local_dir_relative():
    payload = {
        "search_id": "valid-id",
        "local_dir": "path/../../etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "local_dir" in response.text

def test_valid_payload():
    # This might fail because GEMINI_API_KEY is dummy, but it should pass Pydantic validation
    payload = {
        "search_id": "valid_id-123",
        "brief_notes": "test",
        "jd_content": "test"
    }
    # We just want to see it passes validation.
    # It might return 500 or 400 later due to missing keys/service down,
    # but 422 would mean validation failed.
    response = client.post("/api/v1/search/setup", json=payload)
    # If it reached internal logic and failed due to connection error, it will be 500 (per my hardening)
    assert response.status_code in [200, 400, 500]
