from infra.db.api import app
import os
from fastapi.testclient import TestClient
import sys

# Ensure project root is in path
sys.path.append(os.getcwd())


client = TestClient(app)


def test_db_entity_id_validation():
    # Test entity_id validation in /entity/upsert
    payload = {
        "entity_id": "../malicious",
        "current_stage": "test",
        "state": "test",
        "agent_responsible": "test_agent",
        "trace_id": "test_trace"
    }
    response = client.post("/entity/upsert", json=payload)
    print(f"Upsert (invalid entity_id) Response: {response.status_code}")
    assert response.status_code == 422


def test_db_agent_responsible_validation():
    # Test agent_responsible validation
    payload = {
        "entity_id": "valid_id",
        "current_stage": "test",
        "state": "test",
        "agent_responsible": "agent; DROP TABLE users;",
        "trace_id": "test_trace"
    }
    response = client.post("/entity/upsert", json=payload)
    print(
        f"Upsert (invalid agent_responsible) Response: {response.status_code}")
    assert response.status_code == 422


def test_db_valid_payload():
    # Test a valid payload
    payload = {
        "entity_id": "valid-id_123",
        "current_stage": "test",
        "state": "test",
        "agent_responsible": "test-agent",
        "trace_id": "trace_456"
    }
    # Mocking DB call or just letting it fail with 500 if DB is not init'd,
    # but we care about validation (422) vs accepted (not 422).
    response = client.post("/entity/upsert", json=payload)
    print(f"Upsert (valid payload) Response: {response.status_code}")
    assert response.status_code != 422


if __name__ == "__main__":
    try:
        test_db_entity_id_validation()
        test_db_agent_responsible_validation()
        test_db_valid_payload()
        print("DB API security verification PASSED")
    except Exception as e:
        print(f"DB API security verification FAILED: {e}")
        sys.exit(1)
