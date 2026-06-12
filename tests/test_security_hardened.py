from fastapi.testclient import TestClient
from api import app
from unittest.mock import patch

client = TestClient(app)


def test_id_validation_patterns():
    # Test invalid search_id in /api/v1/run
    response = client.post("/api/v1/run", json={
        "search_id": "invalid;path",
        "local_dir": "test"
    })
    assert response.status_code == 422  # Pydantic validation error

    # Test path traversal in search_id
    response = client.post("/api/v1/run", json={
        "search_id": "../root",
        "local_dir": "test"
    })
    assert response.status_code == 422


def test_refine_gem_security():
    # Test valid GEM (whitelisted)
    # Mocking GeminiClient to avoid connection errors to Ollama/Gemini
    with patch("api.GeminiClient.run_gem") as mock_run:
        mock_run.return_value = {"markdown": "Refined prompt", "json": {}}
        response = client.post("/api/v1/gems/refine", json={
            "gem_id": "gem1",
            "instruction": "test"
        })
        # Should not be 403. Might be 200 or 404 if file missing, but 403 is what we check.
        assert response.status_code != 403

    # Test non-whitelisted GEM
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "secret_gem",
        "instruction": "test"
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Access to this GEM is restricted"

    # Test path traversal in gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../config",
        "instruction": "test"
    })
    # Pydantic pattern should catch this first with 422
    assert response.status_code == 422


def test_error_leakage():
    # Trigger an error in /api/v1/run (missing GEMINI_API_KEY or other)
    # We force an error by providing an invalid local_dir but valid IDs
    response = client.post("/api/v1/run", json={
        "search_id": "valid-id",
        "local_dir": "/non/existent/path"
    })

    # It should return 500 with a generic message
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error during pipeline execution"
