from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_pipeline_request_path_traversal_validation():
    # 1. Test invalid search_id (has directory traversal characters)
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../malicious",
            "local_dir": "runs/test"
        }
    )
    assert response.status_code == 422
    assert "search_id" in response.text

    # 2. Test invalid candidate_id
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "candidate_id": "invalid/candidate",
            "local_dir": "runs/test"
        }
    )
    assert response.status_code == 422
    assert "candidate_id" in response.text

    # 3. Test invalid local_dir (contains path traversal)
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "local_dir": "runs/../etc"
        }
    )
    assert response.status_code == 422
    assert "local_dir" in response.text

    # 4. Test absolute local_dir path
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-id",
            "local_dir": "/etc"
        }
    )
    assert response.status_code == 422
    assert "local_dir" in response.text


def test_setup_search_path_traversal_validation():
    # Test invalid search_id in setup_search
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "invalid/path",
            "brief_notes": "test notes",
            "jd_content": "test jd"
        }
    )
    assert response.status_code == 422
    assert "search_id" in response.text


def test_refine_gem_path_traversal_validation():
    # Test invalid gem_id in refine_gem
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "invalid..path",
            "instruction": "refine notes"
        }
    )
    assert response.status_code == 422
    assert "gem_id" in response.text
