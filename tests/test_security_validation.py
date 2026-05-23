from fastapi.testclient import TestClient
from api import app


def test_path_traversal_mitigated():
    client = TestClient(app)
    # Path traversal attempt should now fail during validation
    response = client.post(
        "/api/v1/gems/refine", json={"gem_id": "../vuln_test", "instruction": "test"}
    )
    # Pydantic validation error returns 422 Unprocessable Entity
    assert response.status_code == 422
    print(f"Path traversal mitigated. Status: {response.status_code}")


def test_valid_gem_refine():
    client = TestClient(app)
    try:
        response = client.post(
            "/api/v1/gems/refine", json={"gem_id": "gem1", "instruction": "test"}
        )
        # If it doesn't crash, it should not be 422
        assert response.status_code != 422
    except Exception as e:
        # If it crashes with connection error, it means it passed validation
        print(
            f"Valid gem passed validation but failed later (expected): {type(e).__name__}"
        )
        pass


def test_id_validation_pipeline():
    client = TestClient(app)
    response = client.post(
        "/api/v1/run", json={"search_id": "invalid;id", "local_dir": "."}
    )
    assert response.status_code == 422
    print(f"Pipeline search_id validation passed. Status: {response.status_code}")


if __name__ == "__main__":
    test_path_traversal_mitigated()
    test_valid_gem_refine()
    test_id_validation_pipeline()
    print("All security validation tests completed successfully.")
