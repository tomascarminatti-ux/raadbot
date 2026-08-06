from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_pipeline_request_path_traversal():
    """Verifica que PipelineRequest valide y rechace la manipulación de rutas en ID/carpetas."""
    # 1. search_id malicioso
    response = client.post(
        "/api/v1/run",
        json={"search_id": "../malicious_search", "local_dir": "runs/search_1/inputs"},
    )
    assert response.status_code == 422
    assert "search_id" in response.text

    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "sub/../malicious_search",
            "local_dir": "runs/search_1/inputs",
        },
    )
    assert response.status_code == 422

    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "sub\\..\\malicious_search",
            "local_dir": "runs/search_1/inputs",
        },
    )
    assert response.status_code == 422

    # 2. candidate_id malicioso
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_search",
            "local_dir": "runs/search_1/inputs",
            "candidate_id": "../malicious_cand",
        },
    )
    assert response.status_code == 422
    assert "candidate_id" in response.text

    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_search",
            "local_dir": "runs/search_1/inputs",
            "candidate_id": "sub/../malicious_cand",
        },
    )
    assert response.status_code == 422

    # 3. local_dir con directory traversal (..)
    response = client.post(
        "/api/v1/run", json={"search_id": "valid_search", "local_dir": "../anywhere"}
    )
    assert response.status_code == 422
    assert "local_dir" in response.text

    # 4. local_dir con ruta absoluta (empezando con /)
    response = client.post(
        "/api/v1/run", json={"search_id": "valid_search", "local_dir": "/etc/passwd"}
    )
    assert response.status_code == 422
    assert "local_dir" in response.text

    # 5. local_dir con ruta absoluta de Windows (letra de unidad)
    response = client.post(
        "/api/v1/run",
        json={"search_id": "valid_search", "local_dir": "C:\\Windows\\System32"},
    )
    assert response.status_code == 422
    assert "local_dir" in response.text


def test_setup_search_path_traversal():
    """Verifica que SetupSearchRequest valide y rechace search_id maliciosos."""
    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "../malicious",
            "brief_notes": "test notes",
            "jd_content": "test jd",
        },
    )
    assert response.status_code == 422
    assert "search_id" in response.text

    response = client.post(
        "/api/v1/search/setup",
        json={
            "search_id": "sub/../malicious",
            "brief_notes": "test notes",
            "jd_content": "test jd",
        },
    )
    assert response.status_code == 422


def test_refine_gem_path_traversal():
    """Verifica que RefineRequest valide y rechace gem_id maliciosos."""
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../malicious_gem", "instruction": "refine it"},
    )
    assert response.status_code == 422
    assert "gem_id" in response.text

    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "sub/../malicious_gem", "instruction": "refine it"},
    )
    assert response.status_code == 422


def test_valid_inputs():
    """Verifica que las entradas válidas y bien formadas pasen las validaciones de seguridad básicas."""
    # local_dir relativo válido. Esperamos que pase la validación de Pydantic (no devuelve 422).
    # Sin embargo, fallará más adelante en la ejecución real con 400 por no tener GEMINI_API_KEY configurada.
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid-search-123",
            "local_dir": "runs/non_existent_relative_dir",
        },
    )
    # Assert que no sea un error de validación de esquema (422), sino de la lógica posterior (400)
    assert response.status_code == 400
    assert (
        "GEMINI_API_KEY no configurada" in response.text
        or "no configurada" in response.text
    )
