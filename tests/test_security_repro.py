import pytest
from fastapi.testclient import TestClient
import os
import shutil
from unittest.mock import patch

# Set dummy API key for tests if not set
os.environ["GEMINI_API_KEY"] = "dummy_key"

from api import app

client = TestClient(app)

def test_path_traversal_refine_fixed():
    """Verify that path traversal in /api/v1/gems/refine is blocked by validation"""
    payload = {
        "gem_id": "../traversal_repro",
        "instruction": "test"
    }

    response = client.post("/api/v1/gems/refine", json=payload)
    # Pydantic pattern validation should return 422
    assert response.status_code == 422
    assert "string_pattern_mismatch" in str(response.json())

def test_path_traversal_run_fixed():
    """Verify that path traversal in /api/v1/run is blocked by validation"""
    search_id = "../traversal_run_test"
    payload = {
        "search_id": search_id,
        "local_dir": "non_existent_dir"
    }

    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_local_dir_traversal_fixed():
    """Verify that traversal via local_dir is blocked by validation (including absolute paths)"""
    # Leading slash (absolute path) should be blocked by the new regex
    payload = {
        "search_id": "valid_id",
        "local_dir": "/etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

    # Path climbing (relative) should be blocked
    payload = {
        "search_id": "valid_id",
        "local_dir": "../../etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_valid_requests_still_work():
    """Verify that valid requests still work without destructive side effects"""
    # Refine
    payload = {
        "gem_id": "gem1",
        "instruction": "test"
    }

    # Create a temporary test prompt file to avoid overwriting the real one
    test_prompt_dir = "tests/test_prompts"
    os.makedirs(test_prompt_dir, exist_ok=True)
    test_prompt_path = os.path.join(test_prompt_dir, "gem1.md")
    with open(test_prompt_path, "w") as f:
        f.write("original content")

    # Patch the prompt_path in refine_gem to use our test directory
    with patch("api.os.path.join", side_effect=lambda *args: test_prompt_path if args[0] == "prompts" and args[1] == "gem1.md" else os.path.join(*args)):
        with patch("api.GeminiClient.run_gem") as mock_run:
            mock_run.return_value = {"markdown": "new content"}

            # Ensure it actually uses the patched path
            response = client.post("/api/v1/gems/refine", json=payload)
            assert response.status_code == 200

            # Verify the test file was updated
            with open(test_prompt_path, "r") as f:
                assert f.read() == "new content"

    # Clean up test prompt
    shutil.rmtree(test_prompt_dir)

    # Run
    payload = {
        "search_id": "valid-id_123",
        "local_dir": "runs/test_dir"
    }
    # This might fail with 400 because local_dir doesn't exist, but it should NOT be 422
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code != 422
