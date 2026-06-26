import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api import app
import config

client = TestClient(app)

def test_path_traversal_run_pipeline():
    """Verifica que intentos de path traversal en /api/v1/run sean rechazados."""
    payload = {
        "search_id": "../evil",
        "local_dir": "valid_dir"
    }
    response = client.post("/api/v1/run", json=payload)
    # Pydantic validation returns 422 for pattern mismatch
    assert response.status_code == 422
    assert "pattern" in response.text.lower()

def test_path_traversal_setup_search():
    """Verifica que intentos de path traversal en /api/v1/search/setup sean rechazados."""
    payload = {
        "search_id": "valid-id/../../etc/passwd",
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422

def test_path_traversal_refine_gem():
    """Verifica que intentos de path traversal en /api/v1/gems/refine sean rechazados."""
    payload = {
        "gem_id": "gem1/../secret",
        "instruction": "make it better"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422

@patch("agent.gemini_client.GeminiClient.run_gem")
def test_valid_ids_accepted(mock_run_gem):
    """Verifica que IDs válidos pasen la validación de esquema."""
    mock_run_gem.return_value = {"markdown": "Prompt refinado", "data": {}}

    payload = {
        "gem_id": "gem1",
        "instruction": "test"
    }

    response = client.post("/api/v1/gems/refine", json=payload)
    # If it passes Pydantic, it should not be 422.
    # It might be 404 if gem1.md doesn't exist, but that's fine for schema testing.
    assert response.status_code in [200, 404, 500]
