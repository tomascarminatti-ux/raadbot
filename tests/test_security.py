from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open
from api import app

client = TestClient(app)


def test_pipeline_request_path_traversal():
    """Verify that search_id is validated against path traversal patterns."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../evil",
            "local_dir": "test"
        }
    )
    # Pydantic should block this with 422
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.text


def test_pipeline_local_dir_path_traversal():
    """Verify that local_dir is validated against path traversal patterns."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "local_dir": "../etc/passwd"
        }
    )
    assert response.status_code == 422
    assert "Path traversal detected" in response.text


def test_setup_search_path_traversal():
    """Verify that search_id in setup is validated."""
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "invalid/id",
            "brief_notes": "test",
            "jd_content": "test"
        }
    )
    assert response.status_code == 422


def test_refine_gem_path_traversal():
    """Verify that gem_id in refine is validated by pattern."""
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "sub/folder",
            "instruction": "test"
        }
    )
    assert response.status_code == 422


def test_refine_gem_whitelist():
    """Verify that gem_id must be in the ALLOWED_GEMS whitelist."""
    # Pattern is OK, but not in whitelist
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "valid_id_but_not_allowed",
            "instruction": "test"
        }
    )
    assert response.status_code == 403
    assert "GEM not allowed for refinement" in response.text


@patch("api.GeminiClient")
@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data="current prompt")
def test_refine_gem_success(mock_file, mock_exists, mock_gemini):
    """Verify successful refinement with mocked dependencies."""
    mock_exists.return_value = True

    # Mock Gemini result
    mock_instance = mock_gemini.return_value
    mock_instance.run_gem.return_value = {"markdown": "new refined prompt", "raw": "new refined prompt"}

    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "gem1",
            "instruction": "make it better"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["new_prompt"] == "new refined prompt"

    # Verify file was written
    mock_file().write.assert_called_with("new refined prompt")


def test_pipeline_error_leakage():
    """Verify that internal errors don't leak details."""
    with patch("api.run_pipeline", side_effect=Exception("Secret internal error details")):
        response = client.post(
            "/api/v1/run",
            json={
                "search_id": "valid-id",
                "local_dir": "test"
            }
        )
        assert response.status_code == 500
        assert "Internal server error during pipeline execution" in response.text
        assert "Secret internal error details" not in response.text
