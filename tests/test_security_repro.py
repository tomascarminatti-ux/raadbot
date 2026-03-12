
import os
import sys
from fastapi.testclient import TestClient
from api import app
from infra.db.api import app as db_app

client = TestClient(app)
db_client = TestClient(db_app)


def test_path_traversal_search_id():
    # search_id that tries to go out of 'runs'
    payload = {
        "search_id": "../evil_run",
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422  # Unprocessable Entity due to Field pattern
    assert not os.path.exists("evil_run")


def test_path_traversal_refine_gem():
    payload = {
        "gem_id": "../api",
        "instruction": "refine"
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422


def test_path_traversal_local_dir():
    payload = {
        "search_id": "valid_id",
        "local_dir": "../etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422


def test_absolute_path_local_dir():
    payload = {
        "search_id": "valid_id",
        "local_dir": "/etc/passwd"
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422


def test_db_entity_id_validation():
    payload = {
        "entity_id": "../malicious",
        "current_stage": "test",
        "state": "test",
        "agent_responsible": "test",
        "trace_id": "test"
    }
    response = db_client.post("/entity/upsert", json=payload)
    assert response.status_code == 422


if __name__ == "__main__":
    # Run tests manually
    try:
        test_path_traversal_search_id()
        test_path_traversal_refine_gem()
        test_path_traversal_local_dir()
        test_absolute_path_local_dir()
        test_db_entity_id_validation()
        print("All security tests passed!")
    except AssertionError as e:
        print(f"Security test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during testing: {e}")
        sys.exit(1)
