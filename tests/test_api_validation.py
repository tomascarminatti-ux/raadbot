import pytest
from fastapi.testclient import TestClient
from api import app, PipelineRequest, SetupSearchRequest, RefineRequest, validate_identifier, validate_path, validate_webhook

client = TestClient(app)


def test_validate_identifier():
    assert validate_identifier("valid_id-123") == "valid_id-123"
    assert validate_identifier(None) is None

    with pytest.raises(ValueError, match="Invalid identifier format"):
        validate_identifier("invalid/id")

    with pytest.raises(ValueError, match="Invalid identifier format"):
        validate_identifier("../etc/passwd")


def test_validate_path():
    assert validate_path("data/inputs") == "data/inputs"
    assert validate_path(None) is None

    with pytest.raises(ValueError, match="Directory traversal attempt"):
        validate_path("../etc/passwd")

    with pytest.raises(ValueError, match="Directory traversal attempt"):
        validate_path("/etc/passwd")

    with pytest.raises(ValueError, match="Directory traversal attempt"):
        validate_path("C:\\Windows\\System32")


def test_validate_webhook():
    assert validate_webhook("https://hooks.slack.com/services/123/456") == "https://hooks.slack.com/services/123/456"
    assert validate_webhook(None) is None

    with pytest.raises(ValueError, match="Webhook URL must use http or https scheme"):
        validate_webhook("file:///etc/passwd")

    with pytest.raises(ValueError, match="SSRF protection: webhook URL cannot point to localhost"):
        validate_webhook("http://localhost:8080/callback")

    with pytest.raises(ValueError, match="SSRF protection: webhook URL cannot point to localhost"):
        validate_webhook("http://127.0.0.1:8080/callback")

    with pytest.raises(ValueError, match="SSRF protection: webhook URL cannot point to private or loopback IP address"):
        validate_webhook("http://192.168.1.1/callback")


def test_api_pipeline_validation():
    # Valid payload
    valid_payload = {
        "search_id": "search_123",
        "local_dir": "data/search123",
        "candidate_id": "cand_001",
        "webhook_url": "https://example.com/webhook"
    }
    # Test request parsing directly on model
    req = PipelineRequest(**valid_payload)
    assert req.search_id == "search_123"

    # Path traversal in search_id
    res = client.post("/api/v1/run", json={
        "search_id": "../invalid_search",
        "local_dir": "data/search123"
    })
    assert res.status_code == 422

    # Path traversal in local_dir
    res = client.post("/api/v1/run", json={
        "search_id": "search_123",
        "local_dir": "../../../etc"
    })
    assert res.status_code == 422

    # SSRF in webhook_url
    res = client.post("/api/v1/run", json={
        "search_id": "search_123",
        "local_dir": "data/search123",
        "webhook_url": "http://10.0.0.1/internal"
    })
    assert res.status_code == 422


def test_api_setup_validation():
    # Invalid search_id
    res = client.post("/api/v1/search/setup", json={
        "search_id": "search/123",
        "brief_notes": "notes",
        "jd_content": "jd"
    })
    assert res.status_code == 422


def test_api_refine_validation():
    # Invalid gem_id path traversal attempt
    res = client.post("/api/v1/gems/refine", json={
        "gem_id": "../../gem1",
        "instruction": "make it short"
    })
    assert res.status_code == 422
