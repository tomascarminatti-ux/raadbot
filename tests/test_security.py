from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_pipeline_request_path_traversal_search_id():
    # search_id containing path traversal or invalid characters should fail with 422
    payloads = [
        {"search_id": "../etc", "local_dir": "runs/test"},
        {"search_id": "..\\etc", "local_dir": "runs/test"},
        {"search_id": "test/sub", "local_dir": "runs/test"},
        {"search_id": "test$", "local_dir": "runs/test"},
        {"search_id": "test id", "local_dir": "runs/test"},
    ]
    for p in payloads:
        response = client.post("/api/v1/run", json=p)
        assert response.status_code == 422, f"Payload {p} should have been rejected"
        assert "detail" in response.json()


def test_pipeline_request_path_traversal_local_dir():
    # local_dir containing path traversal or absolute paths should fail with 422
    payloads = [
        {"search_id": "test-search", "local_dir": "../etc"},
        {"search_id": "test-search", "local_dir": "/etc/passwd"},
        {"search_id": "test-search", "local_dir": "C:/Windows"},
        {"search_id": "test-search", "local_dir": "sub/../dir"},
    ]
    for p in payloads:
        response = client.post("/api/v1/run", json=p)
        assert response.status_code == 422, f"Payload {p} should have been rejected"
        assert "detail" in response.json()


def test_pipeline_request_path_traversal_candidate_id():
    # candidate_id containing traversal should fail with 422
    payloads = [
        {
            "search_id": "test-search",
            "local_dir": "runs/test",
            "candidate_id": "../etc",
        },
        {
            "search_id": "test-search",
            "local_dir": "runs/test",
            "candidate_id": "can/didate",
        },
    ]
    for p in payloads:
        response = client.post("/api/v1/run", json=p)
        assert response.status_code == 422, f"Payload {p} should have been rejected"
        assert "detail" in response.json()


def test_setup_search_path_traversal_search_id():
    # search_id in setup endpoint containing traversal should fail with 422
    payloads = [
        {"search_id": "../traversal", "brief_notes": "notes", "jd_content": "jd"},
        {"search_id": "sub/folder", "brief_notes": "notes", "jd_content": "jd"},
    ]
    for p in payloads:
        response = client.post("/api/v1/search/setup", json=p)
        assert response.status_code == 422, f"Payload {p} should have been rejected"
        assert "detail" in response.json()


def test_refine_gem_invalid_gem_id():
    # gem_id containing traversal or invalid name should fail with 422
    payloads = [
        {"gem_id": "../gem1", "instruction": "Make it strict"},
        {"gem_id": "gem6", "instruction": "Make it strict"},
        {"gem_id": "invalid_gem", "instruction": "Make it strict"},
    ]
    for p in payloads:
        response = client.post("/api/v1/gems/refine", json=p)
        assert response.status_code == 422, f"Payload {p} should have been rejected"
        assert "detail" in response.json()


def test_valid_safe_identifiers():
    # Verify that valid strings with alphanumeric, dashes or underscores are correctly processed (not raising 422)
    # They might fail on missing keys (or missing configuration) or actual pipeline setup,
    # but they should pass Pydantic's initial validation layer.
    p1 = {"search_id": "valid_search-123", "local_dir": "runs/test"}
    # This should pass Pydantic validation (it might return 400 because of missing GEMINI_API_KEY / files, but not 422)
    response = client.post("/api/v1/run", json=p1)
    assert response.status_code != 422
