import pytest
from fastapi.testclient import TestClient
from api import app

@pytest.fixture
def client():
    return TestClient(app)

def test_path_traversal_search_id(client):
    """Verifica que search_id con path traversal sea rechazado."""
    response = client.post("/api/v1/run", json={
        "search_id": "../evil",
        "local_dir": "valid_dir"
    })
    assert response.status_code == 422
    assert "search_id" in response.json()["detail"][0]["loc"]

def test_path_traversal_local_dir(client):
    """Verifica que local_dir con path traversal sea rechazado."""
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "../evil"
    })
    assert response.status_code == 422
    assert "local_dir" in response.json()["detail"][0]["loc"]

def test_path_traversal_candidate_id(client):
    """Verifica que candidate_id con path traversal sea rechazado."""
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "valid_dir",
        "candidate_id": "../evil"
    })
    assert response.status_code == 422
    assert "candidate_id" in response.json()["detail"][0]["loc"]

def test_path_traversal_gem_id(client):
    """Verifica que gem_id con path traversal sea rechazado."""
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../config",
        "instruction": "make it stricter"
    })
    assert response.status_code == 422
    assert "gem_id" in response.json()["detail"][0]["loc"]

def test_invalid_characters_search_id(client):
    """Verifica que search_id con caracteres inválidos sea rechazado."""
    response = client.post("/api/v1/run", json={
        "search_id": "search; rm -rf /",
        "local_dir": "valid_dir"
    })
    assert response.status_code == 422

def test_valid_identifiers(client):
    """Verifica que identificadores válidos sean aceptados (y pasen a la lógica de negocio)."""
    # En este caso esperamos 400 porque no hay API KEY o 404 porque no existe el dir,
    # pero NO 422 (que es el error de validación de esquema).
    response = client.post("/api/v1/run", json={
        "search_id": "valid-search_123",
        "local_dir": "valid-dir_456"
    })
    assert response.status_code != 422
