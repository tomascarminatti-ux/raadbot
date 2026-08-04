from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

def test_pipeline_request_path_traversal():
    # Test path traversal in search_id
    payload = {
        "search_id": "../malicious",
        "drive_folder": "some_folder"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text

    # Test path traversal in candidate_id
    payload = {
        "search_id": "valid_id",
        "drive_folder": "some_folder",
        "candidate_id": "../../etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "candidate_id" in response.text

    # Test path traversal in local_dir
    payload = {
        "search_id": "valid_id",
        "local_dir": "../../etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "local_dir" in response.text

    # Test absolute path / windows absolute path in local_dir
    payload = {
        "search_id": "valid_id",
        "local_dir": "/absolute/path"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "local_dir" in response.text

    payload = {
        "search_id": "valid_id",
        "local_dir": "C:\\Windows\\System32"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "local_dir" in response.text

def test_setup_search_path_traversal():
    # Test path traversal in search_id
    payload = {
        "search_id": "..\\invalid",
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text

def test_refine_gem_path_traversal():
    # Test path traversal in gem_id
    payload = {
        "gem_id": "gem1/../invalid",
        "instruction": "refine it"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "gem_id" in response.text

def test_valid_inputs_allowed():
    # Verify a valid request doesn't fail with Pydantic validation (422)
    # It might fail with 400 (e.g. missing credentials or folder not found), but not 422.
    payload = {
        "search_id": "VALID-SEARCH_01",
        "local_dir": "runs/test_gem6"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code != 422
