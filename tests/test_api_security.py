from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_pipeline_request_valid():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_search_123",
            "local_dir": "runs/test_dir",
            "candidate_id": "cand_1",
        },
    )
    # Validation passes; failure happens further down if dir missing
    assert response.status_code != 422


def test_pipeline_request_path_traversal_search_id():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../invalid_search",
            "local_dir": "runs/test_dir",
        },
    )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(
        "Identifier contains invalid characters" in str(e) for e in errors
    )


def test_pipeline_request_path_traversal_local_dir():
    invalid_dirs = [
        "../etc/passwd",
        "../../runs",
        "/etc/passwd",
        "C:\\Windows\\System32",
    ]
    for inv_dir in invalid_dirs:
        response = client.post(
            "/api/v1/run",
            json={
                "search_id": "valid_search",
                "local_dir": inv_dir,
            },
        )
        assert response.status_code == 422, f"Failed: {inv_dir}"


def test_setup_search_path_traversal():
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../../bad_search",
            "brief_notes": "notes",
            "jd_content": "jd",
        },
    )
    assert response.status_code == 422


def test_refine_gem_path_traversal():
    invalid_gem_ids = [
        "../templates/dashboard",
        "../../etc/passwd",
        "gem1/../../secret",
    ]
    for gem_id in invalid_gem_ids:
        response = client.post(
            "/api/v1/gems/refine",
            json={
                "gem_id": gem_id,
                "instruction": "Make concise",
            },
        )
        assert response.status_code == 422, f"Failed: {gem_id}"
