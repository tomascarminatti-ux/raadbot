
import os
import shutil
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Mock GeminiClient and other dependencies before importing app
with patch('agent.gemini_client.GeminiClient'), \
     patch('agent.gem6.orchestrator.GEM6Orchestrator'), \
     patch('agent.drive_client.DriveClient'):
    from api import app

client = TestClient(app)

def test_path_traversal_setup_search_blocked():
    evil_path = "../evil_dir_traversal"

    with patch('api.GeminiClient') as MockGeminiClient:
        response = client.post("/api/v1/search/setup", json={
            "search_id": evil_path,
            "brief_notes": "test",
            "jd_content": "test"
        })

        print(f"Response status: {response.status_code}")
        # Expecting 422 Unprocessable Entity due to validation failure
        assert response.status_code == 422

    assert not os.path.exists("evil_dir_traversal")
    assert not os.path.exists("runs/../evil_dir_traversal")
    print("SUCCESS: Path traversal blocked by validation.")

def test_valid_path_allowed():
    valid_path = "valid-search_123"

    with patch('api.GeminiClient') as MockGeminiClient:
        mock_instance = MockGeminiClient.return_value
        mock_instance.run_gem.return_value = {
            "data": {"mandate_summary": "ok"},
            "markdown": "ok",
            "raw": "ok",
            "usage": {"prompt_tokens": 0, "candidates_tokens": 0, "total_tokens": 0, "finish_reason": "STOP"}
        }

        response = client.post("/api/v1/search/setup", json={
            "search_id": valid_path,
            "brief_notes": "test",
            "jd_content": "test"
        })

        assert response.status_code == 200

    # Cleanup created dir
    if os.path.exists(os.path.join("runs", valid_path)):
        shutil.rmtree(os.path.join("runs", valid_path))
    print("SUCCESS: Valid path allowed.")

if __name__ == "__main__":
    try:
        test_path_traversal_setup_search_blocked()
        test_valid_path_allowed()
    except AssertionError as e:
        print(f"FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)
