from fastapi.testclient import TestClient
from api import app
from unittest.mock import patch, mock_open


client = TestClient(app)


def test_search_id_regex_validation():
    # Attempt with invalid search_id (contains dots and slashes)
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../../evil",
            "brief_notes": "test",
            "jd_content": "test"
        }
    )
    # Pydantic should reject this before it reaches the endpoint logic
    assert response.status_code == 422


def test_local_dir_regex_validation():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "../secrets"
        }
    )
    assert response.status_code == 422


def test_candidate_id_regex_validation():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_id",
            "local_dir": "valid_dir",
            "candidate_id": "bad/path"
        }
    )
    assert response.status_code == 422


def test_gem_id_regex_validation():
    # Attempt with invalid gem_id in refine endpoint
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "gem1; rm -rf /", "instruction": "test"}
    )
    assert response.status_code == 422


def test_gem_id_whitelist_validation():
    # Attempt with valid regex but non-whitelisted GEM ID
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "gem6", "instruction": "test"}
    )
    # This should be caught by our manual check in the endpoint
    assert response.status_code == 403
    assert response.json()["detail"] == "Access to this GEM is not allowed"


def test_refine_gem_valid_whitelisted():
    # Test a valid, whitelisted GEM to ensure it still works (with mocking)
    with patch("api.GeminiClient") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.run_gem.return_value = {"markdown": "Refined prompt content"}

        # Mocking the file open for both reading the existing and writing the new
        m = mock_open(read_data="Original prompt content")
        with patch("builtins.open", m):
            with patch("os.path.exists", return_value=True):
                response = client.post(
                    "/api/v1/gems/refine",
                    json={"gem_id": "gem1", "instruction": "make it better"}
                )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
