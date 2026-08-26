from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_pipeline_run_validates_search_id_path_traversal():
    response = client.post(
        "/api/v1/run",
        json={"search_id": "../evil_dir", "local_dir": "runs/test_search"},
    )
    assert response.status_code == 422
    assert "search_id" in response.text


def test_pipeline_run_validates_candidate_id_path_traversal():
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_search",
            "candidate_id": "../../etc/passwd",
            "local_dir": "runs/test_search",
        },
    )
    assert response.status_code == 422
    assert "candidate_id" in response.text


def test_pipeline_run_validates_local_dir_path_traversal():
    response = client.post(
        "/api/v1/run",
        json={"search_id": "valid_search", "local_dir": "../../../etc"},
    )
    assert response.status_code == 422
    assert "local_dir" in response.text


def test_search_setup_validates_search_id_path_traversal():
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../malicious_id",
            "brief_notes": "notes",
            "jd_content": "jd",
        },
    )
    assert response.status_code == 422
    assert "search_id" in response.text


def test_gems_refine_validates_gem_id_path_traversal():
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../gem1", "instruction": "Make it better"},
    )
    assert response.status_code == 422
    assert "gem_id" in response.text


def test_valid_request_format_passes_validation():
    # Model instantiation test for valid identifiers
    from api import PipelineRequest

    req = PipelineRequest(
        search_id="valid-search_123",
        local_dir="runs/valid_dir",
        candidate_id="cand_1",
    )
    assert req.search_id == "valid-search_123"
    assert req.candidate_id == "cand_1"
