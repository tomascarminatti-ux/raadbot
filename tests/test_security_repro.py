import os
from fastapi.testclient import TestClient

# Mock config before importing app
os.environ["GEMINI_API_KEY"] = "fake_key"
os.environ["LLM_PROVIDER"] = "gemini"

from api import app  # noqa: E402

client = TestClient(app)


def test_path_traversal_refine():
    # Attempt to read a file outside of prompts/ using refine_gem logic
    # Now it should fail validation because of the pattern "^[a-zA-Z0-9_-]+$"
    response = client.post(
        "/api/v1/gems/refine", json={"gem_id": "../test_secret", "instruction": "test"}
    )

    print(f"Response status (traversal refine): {response.status_code}")
    print(f"Response body (traversal refine): {response.json()}")
    assert response.status_code == 422


def test_path_traversal_run_dotdot():
    # PipelineRequest local_dir with ..
    response = client.post(
        "/api/v1/run", json={"search_id": "test_search", "local_dir": "runs/../etc"}
    )
    print(f"Response status (traversal run ..): {response.status_code}")
    print(f"Response body (traversal run ..): {response.json()}")
    assert response.status_code == 422


def test_path_traversal_run_absolute():
    # PipelineRequest local_dir with /
    response = client.post(
        "/api/v1/run", json={"search_id": "test_search", "local_dir": "/etc"}
    )
    print(f"Response status (traversal run absolute): {response.status_code}")
    print(f"Response body (traversal run absolute): {response.json()}")
    assert response.status_code == 422


def test_error_hardening_refine():
    # Refine valid gem but fails due to fake key
    response = client.post(
        "/api/v1/gems/refine", json={"gem_id": "gem1", "instruction": "make it better"}
    )
    print(f"Response status (error hardening refine): {response.status_code}")
    print(f"Response body (error hardening refine): {response.json()}")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred during GEM refinement."


if __name__ == "__main__":
    test_path_traversal_refine()
    test_path_traversal_run_dotdot()
    test_path_traversal_run_absolute()
    test_error_hardening_refine()
