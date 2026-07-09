import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# Set environment variables to avoid some initialization issues if any
os.environ["GEMINI_API_KEY"] = "fake_key"

from api import app

client = TestClient(app)

def test_pipeline_request_traversal_search_id():
    # search_id with traversal should be rejected with 422
    response = client.post("/api/v1/run", json={
        "search_id": "../traversal",
        "local_dir": "data/test"
    })
    # If it passes validation, it might try to create a directory or fail later
    # We want 422 from Pydantic
    assert response.status_code == 422

def test_pipeline_request_traversal_local_dir():
    # local_dir with traversal should be rejected with 422
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "../../../etc/passwd"
    })
    assert response.status_code == 422

def test_setup_search_traversal_search_id():
    with patch("agent.gemini_client.GeminiClient.run_gem") as mock_run:
        mock_run.return_value = {"data": {}, "markdown": ""}
        response = client.post("/api/v1/search/setup", json={
            "search_id": "valid/id",
            "brief_notes": "notes",
            "jd_content": "jd"
        })
        assert response.status_code == 422

def test_refine_gem_traversal_gem_id():
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../config",
        "instruction": "test"
    })
    assert response.status_code == 422

def test_pipeline_request_valid():
    with patch("api.run_pipeline") as mock_run:
        mock_run.return_value = {"status": "success", "search_id": "valid_id", "output_dir": "runs/valid_id/outputs", "summary": {}}
        response = client.post("/api/v1/run", json={
            "search_id": "valid_id",
            "local_dir": "data/test"
        })
        assert response.status_code == 200
