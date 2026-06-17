from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_security_hardening():
    # 1. Path traversal (blocked by Pydantic pattern)
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../README",
        "instruction": "test"
    })
    assert response.status_code == 422

    # 2. Non-whitelisted but valid pattern (blocked by whitelist)
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "secret_file",
        "instruction": "test"
    })
    assert response.status_code == 403

    # 3. Path traversal in PipelineRequest
    response = client.post("/api/v1/run", json={
        "search_id": "../evil",
        "local_dir": "test"
    })
    assert response.status_code == 422

    # 4. Path traversal in setup_search
    response = client.post("/api/v1/search/setup", json={
        "search_id": "invalid/id",
        "brief_notes": "test",
        "jd_content": "test"
    })
    assert response.status_code == 422
