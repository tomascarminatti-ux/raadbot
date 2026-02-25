from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_path_traversal_search_id():
    # Attempt to use a path traversal in search_id
    response = client.post("/api/v1/run", json={
        "search_id": "../evil",
        "local_dir": "runs"
    })
    # Pydantic validation error returns 422
    assert response.status_code == 422
    assert "Path traversal detected" in response.text


def test_ssrf_webhook_url():
    # Attempt to use a local IP in webhook_url
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "runs",
        "webhook_url": "http://127.0.0.1:8000/danger"
    })
    # Should return 422 if SSRF protection is in place
    assert response.status_code == 422
    assert "SSRF detected" in response.text


def test_security_headers():
    response = client.get("/health")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in response.headers
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]


if __name__ == "__main__":
    pass
