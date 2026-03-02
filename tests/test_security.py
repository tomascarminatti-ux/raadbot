from fastapi.testclient import TestClient
from api import app


client = TestClient(app)


def test_run_pipeline_path_traversal_search_id():
    # Attempting to use a search_id that goes out of the runs directory
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "../../../evil",
            "local_dir": "some/path"
        }
    )
    # Currently this might return 400 (if it fails later) or 200 (if it "succeeds" in creating the dir)
    # We WANT it to return 422 (Unprocessable Entity) after we add validation
    assert response.status_code == 422


def test_run_pipeline_path_traversal_local_dir():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "normal_id",
            "local_dir": "/etc"
        }
    )
    assert response.status_code == 422


def test_setup_search_path_traversal():
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "test/../../traversal",
            "brief_notes": "test",
            "jd_content": "test"
        }
    )
    assert response.status_code == 422


def test_refine_gem_path_traversal():
    response = client.post(
        "/api/v1/gems/refine",
        json={
            "gem_id": "../config",
            "instruction": "delete everything"
        }
    )
    assert response.status_code == 422
