
import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_refine_gem_path_traversal_regex():
    # Attempt to access a file outside the prompts directory using path traversal
    # The regex ^[a-zA-Z0-9_-]+$ should block this with 422
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../README",
        "instruction": "test"
    })
    assert response.status_code == 422
    assert "string_pattern_mismatch" in str(response.json())

def test_pipeline_run_path_traversal_validator():
    # local_dir is validated by custom field_validator
    # It should block "..", "/", and "C:"

    # Test ".."
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "path/../traversal"
    })
    assert response.status_code == 422
    assert "Ruta local_dir no permitida por seguridad" in str(response.json())

    # Test absolute path "/"
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "/absolute/path"
    })
    assert response.status_code == 422
    assert "Ruta local_dir no permitida por seguridad" in str(response.json())

def test_setup_search_invalid_id():
    # search_id should only allow alphanumeric, _, and -
    response = client.post("/api/v1/search/setup", json={
        "search_id": "invalid;id",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422
    assert "string_pattern_mismatch" in str(response.json())

def test_valid_inputs_pass_validation():
    # Ensure we didn't break valid inputs
    # We mock the actual execution since we only care about validation here
    # Note: run_pipeline and setup_search might fail later due to missing files/keys,
    # but they should PASS validation (not return 422)

    response = client.post("/api/v1/run", json={
        "search_id": "valid-id_123",
        "local_dir": "valid/path"
    })
    # Should not be 422
    assert response.status_code != 422
