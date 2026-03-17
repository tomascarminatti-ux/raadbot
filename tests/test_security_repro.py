
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

# Set up environment variables for testing
os.environ["LLM_PROVIDER"] = "gemini"
os.environ["GEMINI_API_KEY"] = "fake-key"

from api import app
import api
import agent.gemini_client

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_gemini(monkeypatch):
    # Mock the class instance itself
    mock_gemini_instance = MagicMock()
    mock_run_gem = MagicMock(return_value={
        "json": {"action": "finalize"},
        "markdown": "hacked",
        "raw": "hacked",
        "usage": {"prompt_tokens": 0, "candidates_tokens": 0, "total_tokens": 0, "finish_reason": "STOP"}
    })
    mock_gemini_instance.run_gem = mock_run_gem

    # We must mock the class so when api.py does GeminiClient(api_key=...) it returns our mock
    monkeypatch.setattr(agent.gemini_client, "GeminiClient", MagicMock(return_value=mock_gemini_instance))
    monkeypatch.setattr(api, "GeminiClient", MagicMock(return_value=mock_gemini_instance))

    return mock_run_gem

def test_refine_gem_path_traversal_blocked():
    # Attempting path traversal should now return 422
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../vulnerable_test", "instruction": "test"}
    )
    assert response.status_code == 422

def test_pipeline_run_path_traversal_blocked():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../../evil",
            "local_dir": "any",
            "model": "any"
        }
    )
    assert response.status_code == 422

def test_valid_ids_accepted():
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "gem1", "instruction": "test"}
    )
    # It might be 404 if the file gem1.md doesn't exist in the test env, but NOT 422.
    assert response.status_code != 422

if __name__ == "__main__":
    # To run manually:
    try:
        test_refine_gem_path_traversal_blocked()
        test_pipeline_run_path_traversal_blocked()
        test_valid_ids_accepted()
        print("Tests passed: Vulnerabilities blocked (returned 422)")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
