from fastapi.testclient import TestClient
from api import app
import pytest

client = TestClient(app)

def test_path_traversal_refine_gem():
    # Attempt to access/overwrite a file outside the prompts directory
    # Now it should be caught by Pydantic validation (422)
    response = client.post(
        "/api/v1/gems/refine",
        json={"gem_id": "../README", "instruction": "test"}
    )
    assert response.status_code == 422

def test_path_traversal_run_pipeline_search_id():
    # search_id with traversal characters
    response = client.post(
        "/api/v1/run",
        json={"search_id": "../../evil", "local_dir": "safe_dir"}
    )
    assert response.status_code == 422

def test_path_traversal_run_pipeline_local_dir():
    # local_dir with traversal characters
    response = client.post(
        "/api/v1/run",
        json={"search_id": "valid_id", "local_dir": "../../../etc"}
    )
    assert response.status_code == 422

def test_absolute_path_local_dir():
    # absolute path in local_dir
    response = client.post(
        "/api/v1/run",
        json={"search_id": "valid_id", "local_dir": "/etc"}
    )
    assert response.status_code == 422

def test_valid_input():
    # This might still fail with 400 if it proceeds to run_pipeline but doesn't find the directory,
    # but it should PASS Pydantic validation (not 422).
    # Since we don't have a valid API key or real dirs, 400 is expected from the endpoint logic.
    response = client.post(
        "/api/v1/run",
        json={"search_id": "valid-123_ID", "local_dir": "valid_dir"}
    )
    assert response.status_code != 422

if __name__ == "__main__":
    # Manually run if needed
    pytest.main([__file__])
