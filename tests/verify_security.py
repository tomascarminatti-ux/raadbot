import os
import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_local_dir():
    print("\nTesting path traversal in local_dir...")
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "test",
            "local_dir": "/etc"
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 422

def test_path_traversal_search_id():
    print("\nTesting path traversal in search_id...")
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../../evil",
            "brief_notes": "test",
            "jd_content": "test"
        }
    )
    print(f"Status Code: {response.status_code}")
    # print(f"Response: {response.json()}")
    assert response.status_code == 422

def test_ssrf_webhook():
    print("\nTesting SSRF in webhook_url...")
    urls = [
        "http://localhost:22",
        "http://127.0.0.1:8000",
        "http://169.254.169.254/latest/meta-data/",
        "http://192.168.1.1",
        "http://10.0.0.1"
    ]
    for url in urls:
        response = client.post(
            "/api/v1/run",
            json={
                "search_id": "test",
                "local_dir": "runs",
                "webhook_url": url
            }
        )
        print(f"URL {url} -> Status Code: {response.status_code}")
        assert response.status_code == 422

def test_security_headers():
    print("\nTesting security headers...")
    response = client.get("/health")
    headers = response.headers
    print(f"X-Frame-Options: {headers.get('X-Frame-Options')}")
    assert headers.get("X-Frame-Options") == "DENY"
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert "Content-Security-Policy" in headers

if __name__ == "__main__":
    test_path_traversal_local_dir()
    test_path_traversal_search_id()
    test_ssrf_webhook()
    test_security_headers()
