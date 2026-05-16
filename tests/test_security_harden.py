
from fastapi.testclient import TestClient
from api import app

client = TestClient(app, raise_server_exceptions=False)


def test_path_traversal_refine_gem():
    # Attempt to read a file outside the prompts directory
    # The code does: prompt_path = f"prompts/{request.gem_id}.md"
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../config",
        "instruction": "test"
    })
    # Must be blocked by Pydantic validation (422)
    assert response.status_code == 422


def test_path_traversal_run_pipeline():
    response = client.post("/api/v1/run", json={
        "search_id": "../../../etc/passwd",
        "local_dir": "tests"
    })
    assert response.status_code == 422


def test_invalid_search_id_setup():
    response = client.post("/api/v1/search/setup", json={
        "search_id": "invalid/path",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422


def test_error_masking_run_pipeline():
    # Provide valid search_id but something that will cause a crash (e.g. missing local_dir)
    # run_pipeline will raise ValueError if local_dir is missing, which we handle specifically
    response = client.post("/api/v1/run", json={
        "search_id": "valid_id",
        "local_dir": "nonexistent_dir"
    })
    # If it's a ValueError, we might still return 400 with details.
    # But if it was some other unexpected error, it should be 500 masked.
    assert response.status_code in [400, 500]
