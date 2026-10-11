from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api import app

client = TestClient(app)


def test_pipeline_request_valid_input():
    payload = {
        "search_id": "search_123",
        "local_dir": "inputs/search_123",
        "candidate_id": "candidate_1",
    }
    from api import PipelineRequest

    req = PipelineRequest(**payload)
    assert req.search_id == "search_123"
    assert req.candidate_id == "candidate_1"
    assert req.local_dir == "inputs/search_123"


@patch("api.GeminiClient")
def test_pipeline_request_invalid_search_id_path_traversal(mock_gemini):
    response = client.post(
        "/api/v1/run",
        json={"search_id": "../etc/passwd", "local_dir": "valid_dir"},
    )
    assert response.status_code == 422
    assert "Identifier must contain only alphanumeric" in response.text


@patch("api.GeminiClient")
def test_pipeline_request_invalid_local_dir_traversal(mock_gemini):
    response = client.post(
        "/api/v1/run",
        json={"search_id": "search_123", "local_dir": "../sensitive_folder"},
    )
    assert response.status_code == 422
    assert "Invalid local_dir path" in response.text


@patch("api.GeminiClient")
def test_pipeline_request_invalid_candidate_id_traversal(mock_gemini):
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "search_123",
            "local_dir": "valid_dir",
            "candidate_id": "../../candidate",
        },
    )
    assert response.status_code == 422


@patch("api.GeminiClient")
def test_refine_request_invalid_gem_id(mock_gemini):
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../gem1", "instruction": "Make prompt concise"},
    )
    assert response.status_code == 422
    assert "gem_id must contain only alphanumeric" in response.text


@patch("api.GeminiClient")
def test_setup_search_request_invalid_search_id(mock_gemini):
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../search_test",
            "brief_notes": "notes",
            "jd_content": "jd",
        },
    )
    assert response.status_code == 422
