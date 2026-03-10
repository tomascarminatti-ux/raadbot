from fastapi.testclient import TestClient
from api import app


client = TestClient(app)


def test_pipeline_run_path_traversal():
    """Verifica que el endpoint /api/v1/run valide search_id adecuadamente."""
    # Intentamos inyectar un path traversal en search_id
    payload = {
        "search_id": "../../../etc/passwd",
        "local_dir": "inputs",
        "model": "gemini-2.0-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    # Debería devolver 422 por falla de validación de Pydantic
    assert response.status_code == 422


def test_pipeline_run_local_dir_validation():
    """Verifica que local_dir no permita path traversal."""
    payload = {
        "search_id": "valid_id",
        "local_dir": "../forbidden",
        "model": "gemini-2.0-flash"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422


def test_setup_search_path_traversal():
    """Verifica que /api/v1/search/setup valide search_id."""
    payload = {
        "search_id": "malicious/path",
        "brief_notes": "notes",
        "jd_content": "jd"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422


def test_refine_gem_path_traversal():
    """Verifica que /api/v1/gems/refine valide gem_id."""
    payload = {
        "gem_id": "../../config",
        "instruction": "hacker instruction"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422


if __name__ == "__main__":
    # Ejecución manual para verificar el fix
    print("Verificando protecciones (después del fix)...")
    try:
        test_pipeline_run_path_traversal()
        print("✅ /api/v1/run RECHAZA search_id malformado")
        test_pipeline_run_local_dir_validation()
        print("✅ /api/v1/run RECHAZA local_dir con traversal")
        test_setup_search_path_traversal()
        print("✅ /api/v1/search/setup RECHAZA search_id malformado")
        test_refine_gem_path_traversal()
        print("✅ /api/v1/gems/refine RECHAZA gem_id malformado")
        print("\n🎉 Todas las verificaciones de seguridad pasaron.")
    except Exception as e:
        print(f"❌ Error en la verificación: {e}")
