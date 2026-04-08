import pytest
from fastapi.testclient import TestClient
import os

# Set dummy environment variable before importing app to pass startup check
os.environ["GEMINI_API_KEY"] = "dummy"

from api import app

client = TestClient(app)

def test_path_traversal_search_id():
    """Vulnerabilidad: search_id permite salir del directorio runs/"""
    payload = {
        "search_id": "../../../etc/passwd",
        "local_dir": "tests"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422, f"search_id no protegido. Status: {response.status_code}"

def test_path_traversal_local_dir():
    """Vulnerabilidad: local_dir permite leer archivos fuera del scope esperado"""
    payload = {
        "search_id": "valid_id",
        "local_dir": "/etc"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422, f"local_dir no protegido. Status: {response.status_code}"

def test_path_traversal_gem_id():
    """Vulnerabilidad: gem_id permite leer prompts arbitrarios o archivos"""
    payload = {
        "gem_id": "../config",
        "instruction": "refine"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422, f"gem_id no protegido. Status: {response.status_code}"

if __name__ == "__main__":
    # Ejecución rápida manual
    try:
        test_path_traversal_search_id()
        print("✅ search_id PROTEGIDO")
    except AssertionError as e:
        print(f"❌ search_id SIGUE VULNERABLE: {e}")

    try:
        test_path_traversal_local_dir()
        print("✅ local_dir PROTEGIDO")
    except AssertionError as e:
        print(f"❌ local_dir SIGUE VULNERABLE: {e}")

    try:
        test_path_traversal_gem_id()
        print("✅ gem_id PROTEGIDO")
    except AssertionError as e:
        print(f"❌ gem_id SIGUE VULNERABLE: {e}")
