from fastapi.testclient import TestClient
from infra.db.api import app


def test_db_validation():
    client = TestClient(app)
    # Test valid discovery log
    response = client.post(
        "/log/discovery",
        json={
            "entity_id": "valid_id",
            "agent_id": "agent_1",
            "input_ok": True,
            "output_ok": True,
            "time_ms": 100,
            "status": "success",
            "trace_id": "trace-123",
        },
    )
    # 200 or 500 (if DB not init) but not 422
    assert response.status_code != 422
    print(f"DB valid log passed validation. Status: {response.status_code}")
    # Test invalid discovery log (regex fail)
    response = client.post(
        "/log/discovery",
        json={
            "entity_id": "invalid;id",
            "agent_id": "agent_1",
            "input_ok": True,
            "output_ok": True,
            "time_ms": 100,
            "status": "success",
            "trace_id": "trace-123",
        },
    )
    assert response.status_code == 422
    print(f"DB invalid log caught by validation. Status: {response.status_code}")


if __name__ == "__main__":
    test_db_validation()
