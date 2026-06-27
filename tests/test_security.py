import pytest
from fastapi.testclient import TestClient
from api import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.parametrize("endpoint,payload,field", [
    ("/api/v1/run", {"search_id": "../evil", "local_dir": "valid"}, "search_id"),
    ("/api/v1/run", {"search_id": "valid", "local_dir": "../evil"}, "local_dir"),
    ("/api/v1/run", {"search_id": "valid", "local_dir": "valid", "candidate_id": "../evil"}, "candidate_id"),
    ("/api/v1/gems/refine", {"gem_id": "../config", "instruction": "test"}, "gem_id"),
    ("/api/v1/run", {"search_id": "search; rm -rf /", "local_dir": "valid"}, "search_id"),
])
def test_path_traversal_rejection(client, endpoint, payload, field):
    response = client.post(endpoint, json=payload)
    assert response.status_code == 422
    assert field in response.json()["detail"][0]["loc"]

def test_valid_identifiers(client):
    response = client.post("/api/v1/run", json={"search_id": "valid-id_123", "local_dir": "valid-dir"})
    assert response.status_code != 422
