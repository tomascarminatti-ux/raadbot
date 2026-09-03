from fastapi.testclient import TestClient
from api import app, PipelineRequest

client = TestClient(app)


def test_pipeline_request_path_traversal_search_id():
    payload = {
        "search_id": "../../../etc/passwd",
        "local_dir": "valid_dir",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422


def test_pipeline_request_path_traversal_local_dir():
    payload = {
        "search_id": "valid_search_1",
        "local_dir": "../../secret_dir",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422


def test_pipeline_request_candidate_id_traversal():
    payload = {
        "search_id": "valid_search_1",
        "local_dir": "valid_dir",
        "candidate_id": "../candidate_hacked",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422


def test_setup_search_request_path_traversal():
    payload = {
        "search_id": "../../etc/shadow",
        "brief_notes": "notes",
        "jd_content": "jd",
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422


def test_refine_gem_request_path_traversal():
    payload = {
        "gem_id": "../gem_exploit",
        "instruction": "refine",
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422


def test_valid_pipeline_request_model_validation():
    req = PipelineRequest(
        search_id="valid-search_123",
        local_dir="inputs/search_1",
        candidate_id="cand_1",
    )
    assert req.search_id == "valid-search_123"
    assert req.local_dir == "inputs/search_1"
    assert req.candidate_id == "cand_1"
