from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_path_traversal_local_dir():
    """Verifica que el acceso a rutas absolutas en local_dir sea bloqueado."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "test",
            "local_dir": "/etc"
        }
    )
    assert response.status_code == 422
    assert "String should match pattern" in response.text

def test_path_traversal_search_id():
    """Verifica que secuencias de traversal en search_id sean bloqueadas."""
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../../evil",
            "brief_notes": "test",
            "jd_content": "test"
        }
    )
    assert response.status_code == 422

def test_ssrf_webhook():
    """Verifica que URLs de webhook internas o privadas sean bloqueadas."""
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
        assert response.status_code == 422
        assert "Internal webhook URLs are not allowed" in response.text or \
               "Private network webhooks are not allowed" in response.text

def test_security_headers():
    """Verifica que las cabeceras de seguridad estén presentes."""
    response = client.get("/health")
    headers = response.headers
    assert headers.get("x-frame-options") == "DENY"
    assert headers.get("x-content-type-options") == "nosniff"
    assert "content-security-policy" in headers
