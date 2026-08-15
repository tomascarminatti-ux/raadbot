from fastapi.testclient import TestClient

from api import PipelineRequest, RefineRequest, SetupSearchRequest, app

client = TestClient(app)


def test_pipeline_request_path_traversal_validation():
    """Verify that path traversal strings in PipelineRequest search_id or candidate_id are rejected."""
    # Test path traversal in search_id
    payload_search_id = {"search_id": "../../../etc/passwd", "local_dir": "valid_dir"}
    response = client.post("/api/v1/run", json=payload_search_id)
    assert response.status_code == 422

    # Test invalid chars in candidate_id
    payload_candidate = {
        "search_id": "valid_search_id",
        "candidate_id": "../invalid_candidate",
        "local_dir": "valid_dir",
    }
    response = client.post("/api/v1/run", json=payload_candidate)
    assert response.status_code == 422

    # Test path traversal in local_dir
    payload_local_dir = {
        "search_id": "valid_search_id",
        "local_dir": "../sensitive_folder",
    }
    response = client.post("/api/v1/run", json=payload_local_dir)
    assert response.status_code == 422


def test_setup_search_request_path_traversal_validation():
    """Verify that setup_search rejects path traversal search_id values."""
    payload = {
        "search_id": "../../etc/shadow",
        "brief_notes": "test notes",
        "jd_content": "test jd",
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422


def test_refine_gem_request_path_traversal_validation():
    """Verify that refine_gem rejects path traversal gem_id values."""
    payload = {"gem_id": "../prompts/secret", "instruction": "refine prompt"}
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422


def test_valid_requests_schema_pass():
    """Verify that valid alphanumeric inputs pass schema validation without 422 errors."""
    valid_pipeline = PipelineRequest(
        search_id="search_123_test",
        candidate_id="candidate_001",
        local_dir="inputs/search_123",
    )
    assert valid_pipeline.search_id == "search_123_test"
    assert valid_pipeline.candidate_id == "candidate_001"
    assert valid_pipeline.local_dir == "inputs/search_123"

    valid_setup = SetupSearchRequest(
        search_id="search_abc-1", brief_notes="notes", jd_content="jd"
    )
    assert valid_setup.search_id == "search_abc-1"

    valid_refine = RefineRequest(gem_id="gem1", instruction="make concise")
    assert valid_refine.gem_id == "gem1"
