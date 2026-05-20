import os
import shutil
from fastapi.testclient import TestClient
from api import app
from infra.db.api import app as db_app

client = TestClient(app)
db_client = TestClient(db_app)

def test_security_harden():
    # 1. Test api.py - setup_search path traversal
    print("Testing api.py: setup_search path traversal...")
    malicious_id = "../evil_dir"
    payload = {
        "search_id": malicious_id,
        "brief_notes": "test",
        "jd_content": "test"
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✓ Path traversal in setup_search blocked.")

    # 2. Test api.py - trigger_pipeline path traversal
    print("Testing api.py: trigger_pipeline path traversal...")
    payload_run = {
        "search_id": malicious_id,
        "local_dir": "test"
    }
    response = client.post("/api/v1/run", json=payload_run)
    assert response.status_code == 422
    print("✓ Path traversal in trigger_pipeline blocked.")

    # 3. Test api.py - refine_gem path traversal
    print("Testing api.py: refine_gem path traversal...")
    payload_refine = {
        "gem_id": "../../etc/passwd",
        "instruction": "refine"
    }
    response = client.post("/api/v1/gems/refine", json=payload_refine)
    assert response.status_code == 422
    print("✓ Path traversal in refine_gem blocked.")

    # 4. Test infra/db/api.py - upsert_entity path traversal
    print("Testing infra/db/api.py: upsert_entity validation...")
    payload_db = {
        "entity_id": malicious_id,
        "current_stage": "GEM1",
        "state": "PENDING",
        "agent_responsible": "test",
        "trace_id": "valid-trace"
    }
    response = db_client.post("/entity/upsert", json=payload_db)
    assert response.status_code == 422
    print("✓ Invalid entity_id in db/upsert blocked.")

    # 5. Test infra/db/api.py - log_discovery validation
    print("Testing infra/db/api.py: log_discovery validation...")
    payload_log = {
        "entity_id": "valid-id",
        "agent_id": malicious_id,
        "input_ok": True,
        "output_ok": True,
        "time_ms": 100,
        "status": "success",
        "trace_id": "valid-trace"
    }
    response = db_client.post("/log/discovery", json=payload_log)
    assert response.status_code == 422
    print("✓ Invalid agent_id in db/log blocked.")

    # 6. Test error masking in api.py (trigger_pipeline failure)
    print("Testing api.py: error masking...")
    # This will fail because GEMINI_API_KEY is not set or invalid,
    # but we want to see the masked message.
    payload_valid = {
        "search_id": "valid-id",
        "local_dir": "nonexistent"
    }
    # Note: run_pipeline raises ValueError if local_dir not found or no api_key
    # which trigger_pipeline catches and raises 400.
    response = client.post("/api/v1/run", json=payload_valid)
    assert response.status_code == 400
    assert response.json()["detail"] == "Pipeline execution failed"
    print("✓ Error masking in api.py verified.")

    print("\nALL SECURITY TESTS PASSED!")

if __name__ == "__main__":
    try:
        test_security_harden()
    except AssertionError as e:
        print(f"SECURITY TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"AN ERROR OCCURRED: {e}")
        exit(1)
