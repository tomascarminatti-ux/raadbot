import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# Set dummy env vars before importing app
os.environ["GEMINI_API_KEY"] = "dummy_key"

from api import app

client = TestClient(app)

def test_search_id_path_traversal_setup():
    """Test path traversal via search_id in /api/v1/search/setup"""
    payload = {
        "search_id": "../../traversal_setup",
        "brief_notes": "test",
        "jd_content": "test"
    }
    # Before fix: This might return 200 (if it doesn't fail on LLM call) or 500
    # After fix: Should return 422 (Unprocessable Entity) due to Pydantic validation
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422

def test_gem_id_path_traversal_refine():
    """Test path traversal via gem_id in /api/v1/gems/refine"""
    payload = {
        "gem_id": "../secret",
        "instruction": "test"
    }
    # Before fix: Might try to read 'prompts/../secret.md'
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422

def test_search_id_path_traversal_run():
    """Test path traversal via search_id in /api/v1/run"""
    payload = {
        "search_id": "../traversal_run",
        "local_dir": "data/test"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_local_dir_path_traversal_run():
    """Test path traversal via local_dir in /api/v1/run"""
    payload = {
        "search_id": "valid-id",
        "local_dir": "/etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

    payload = {
        "search_id": "valid-id",
        "local_dir": "../../etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_candidate_id_path_traversal_run():
    """Test path traversal via candidate_id in /api/v1/run"""
    payload = {
        "search_id": "valid-id",
        "local_dir": "data/test",
        "candidate_id": "../traversal_candidate"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

if __name__ == "__main__":
    # If run directly, try to see current behavior (will likely fail with 422 AFTER fix)
    # This is useful for manual verification during development.
    import sys
    try:
        test_search_id_path_traversal_setup()
        print("Setup traversal BLOCKED (422)")
    except AssertionError:
        print("Setup traversal ALLOWED (NOT 422)")

    try:
        test_gem_id_path_traversal_refine()
        print("Refine traversal BLOCKED (422)")
    except AssertionError:
        print("Refine traversal ALLOWED (NOT 422)")
