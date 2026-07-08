import os
import pytest
from fastapi.testclient import TestClient
from api import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_path_traversal_refine():
    # Attempt to use invalid ID with dots or slashes
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../api",
        "instruction": "refine"
    })
    # Pydantic validation should catch it and return 422
    assert response.status_code == 422

def test_path_traversal_run():
    response = client.post("/api/v1/run", json={
        "search_id": "../../etc/passwd",
        "local_dir": "data"
    })
    assert response.status_code == 422

def test_path_traversal_run_local_dir():
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "/etc"
    })
    assert response.status_code == 422

    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "../sensitive"
    })
    assert response.status_code == 422

def test_path_traversal_setup():
    response = client.post("/api/v1/search/setup", json={
        "search_id": "../sensitive",
        "brief_notes": "notes",
        "jd_content": "jd"
    })
    assert response.status_code == 422

def test_valid_ids():
    # Mock LLM and other external calls to avoid failures during validation testing
    with patch("api.GeminiClient"), \
         patch("api.load_local_inputs", return_value=({}, {})), \
         patch("api.GEM6Orchestrator") as mock_orch:

        mock_orch.return_value.run_pipeline = MagicMock(return_value=asyncio_future({}))

        # Test valid search_id
        response = client.post("/api/v1/run", json={
            "search_id": "valid-search_123",
            "local_dir": "runs"
        })
        # Should pass validation, might fail later but not 422
        assert response.status_code != 422

def asyncio_future(result):
    import asyncio
    f = asyncio.Future()
    f.set_result(result)
    return f
