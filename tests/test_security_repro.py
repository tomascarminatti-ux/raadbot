import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_pipeline_path_traversal():
    """Verifica que un intento de path traversal en local_dir sea rechazado."""
    payload = {
        "search_id": "test_search",
        "local_dir": "../../etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    # Antes del fix, esto probablemente intente cargar archivos de /etc/passwd y falle con 400 (Value Error)
    # o 500 si no puede leer. Queremos que Pydantic lo rechace con 422.
    assert response.status_code == 422

def test_pipeline_invalid_search_id():
    """Verifica que caracteres inválidos en search_id sean rechazados."""
    payload = {
        "search_id": "test; rm -rf /",
        "local_dir": "inputs"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422

def test_setup_search_invalid_id():
    """Verifica que search_id malformado en setup sea rechazado."""
    payload = {
        "search_id": "invalido/../path",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422

def test_refine_gem_invalid_id():
    """Verifica que gem_id malformado sea rechazado."""
    payload = {
        "gem_id": "gem1; injection",
        "instruction": "refine"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
