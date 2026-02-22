import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from api import app

client = TestClient(app)

def test_path_traversal_search_id():
    response = client.post("/api/v1/search/setup", json={
        "search_id": "../traversal",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422
    assert "Potential path traversal" in response.json()["detail"][0]["msg"]

def test_path_traversal_gem_id():
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../../etc/passwd",
        "instruction": "test"
    })
    assert response.status_code == 422
    assert "Potential path traversal" in response.json()["detail"][0]["msg"]

def test_ssrf_webhook_url_localhost():
    response = client.post("/api/v1/run", json={
        "search_id": "test",
        "webhook_url": "http://localhost:8000/api/v1/run"
    })
    assert response.status_code == 422
    assert "webhook_url must be a public URL" in response.json()["detail"][0]["msg"]

def test_ssrf_webhook_url_private_ip():
    # Test common private IP ranges
    private_ips = [
        "http://192.168.1.1/callback",
        "https://10.0.0.5:8080/hook",
        "http://172.16.0.100/webhook",
        "http://127.0.0.1/evil"
    ]
    for url in private_ips:
        response = client.post("/api/v1/run", json={
            "search_id": "test",
            "webhook_url": url
        })
        assert response.status_code == 422
        assert "webhook_url must be a public URL" in response.json()["detail"][0]["msg"]

@patch("api.GeminiClient")
def test_valid_inputs(mock_gemini):
    # Mock gemini to avoid API key requirement
    mock_gemini.return_value.run_gem.return_value = {"data": {}, "markdown": ""}

    response = client.post("/api/v1/search/setup", json={
        "search_id": "valid-id",
        "brief_notes": "test",
        "jd_content": "test"
    })
    # Now it should be 200 because we mocked Gemini
    assert response.status_code == 200
