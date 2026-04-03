import pytest
from fastapi.testclient import TestClient
import os
import shutil

# Set dummy key for testing
os.environ["GEMINI_API_KEY"] = "dummy"

from api import app

client = TestClient(app)

def test_path_traversal_validation():
    # Test search_id validation
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../evil_dir",
            "local_dir": "tests"
        }
    )
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

    # Test gem_id validation
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "invalid/path",
            "instruction": "test"
        }
    )
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text

def test_local_dir_validation():
    # Test local_dir starting with slash
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "/etc/passwd"
        }
    )
    assert response.status_code == 422

    # Test local_dir with traversal
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "some/../path"
        }
    )
    assert response.status_code == 422

def test_ssrf_validation():
    # Test localhost
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "tests",
            "webhook_url": "http://localhost:8000/callback"
        }
    )
    assert response.status_code == 422
    assert "Webhook URL cannot be localhost" in response.text

    # Test private IP
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "tests",
            "webhook_url": "http://192.168.1.1/callback"
        }
    )
    assert response.status_code == 422
    assert "private or loopback IP address" in response.text

    # Test valid public URL (should pass validation, might fail later if no internet)
    # We just want to see it passes Pydantic validation
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "tests",
            "webhook_url": "https://example.com/callback"
        }
    )
    # It might fail with 400 because 'tests' is not a valid data dir for the pipeline,
    # but it shouldn't be 422 (validation error)
    assert response.status_code != 422
