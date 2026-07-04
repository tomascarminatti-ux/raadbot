
from unittest.mock import patch
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_run_pipeline_search_id():
    # Attempt path traversal via search_id
    response = client.post("/api/v1/run", json={
        "search_id": "../evil",
        "local_dir": "data"
    })
    # Should be blocked by validation (422)
    assert response.status_code == 422

def test_path_traversal_run_pipeline_local_dir():
    # Attempt path traversal via local_dir
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "/etc"
    })
    # Should be blocked by validation (422)
    assert response.status_code == 422

def test_path_traversal_setup_search():
    # Attempt path traversal via search_id
    response = client.post("/api/v1/search/setup", json={
        "search_id": "/tmp/evil",
        "brief_notes": "test",
        "jd_content": "test"
    })
    # Should be blocked by validation (422)
    assert response.status_code == 422

def test_path_traversal_refine_gem():
    # Attempt path traversal via gem_id
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../../etc/passwd",
        "instruction": "test"
    })
    # Should be blocked by validation (422)
    assert response.status_code == 422

def test_valid_ids_pass_validation():
    # We mock run_gem to avoid actual LLM calls and connection errors
    with patch("agent.gemini_client.GeminiClient.run_gem") as mock_run:
        mock_run.return_value = {"data": {}, "markdown": "test"}

        # This should pass Pydantic validation
        response = client.post("/api/v1/search/setup", json={
            "search_id": "valid-id_123",
            "brief_notes": "test",
            "jd_content": "test"
        })
        # 422 Unprocessable Entity is returned by FastAPI when Pydantic validation fails.
        assert response.status_code != 422
        assert response.status_code == 200
