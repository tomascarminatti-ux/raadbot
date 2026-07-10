import os
import sys
from fastapi.testclient import TestClient

# Mock environment variables
os.environ["GEMINI_API_KEY"] = "mock_key"

# Ensure we can import api.py
sys.path.append(os.getcwd())

try:
    from api import app
except ImportError as e:
    print(f"Error importing app: {e}")
    sys.exit(1)

client = TestClient(app)

def test_vulnerability(name, endpoint, payload, expected_blocked=True):
    print(f"--- Testing: {name} ---")
    try:
        response = client.post(endpoint, json=payload)
        print(f"Endpoint: {endpoint}")
        print(f"Payload: {payload}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")

        if expected_blocked:
            if response.status_code == 422:
                print("✅ RESULT: Blocked by Pydantic validation (as expected).")
            elif response.status_code >= 400:
                print(f"✅ RESULT: Blocked with status {response.status_code}.")
            else:
                print("❌ RESULT: VULNERABLE! Request was not blocked.")
        else:
            if response.status_code < 400:
                print("✅ RESULT: Success (as expected).")
            else:
                print(f"❌ RESULT: Failed with status {response.status_code}.")
    except Exception as e:
        if expected_blocked and "Permission denied" in str(e):
             print(f"❌ RESULT: VULNERABLE! Attempted path traversal led to: {e}")
        else:
            print(f"❌ ERROR during test: {e}")
    print("\n")

if __name__ == "__main__":
    print("Running Security Vulnerability Reproduction Script\n")

    # 1. Path Traversal in search_id (PipelineRequest)
    test_vulnerability(
        "Path Traversal in search_id (/api/v1/run)",
        "/api/v1/run",
        {"search_id": "../vulnerable_search", "local_dir": "prompts"}
    )

    # 2. Path Traversal in local_dir (PipelineRequest)
    test_vulnerability(
        "Path Traversal in local_dir (/api/v1/run)",
        "/api/v1/run",
        {"search_id": "test_search", "local_dir": "/etc"}
    )

    # 3. Path Traversal in search_id (SetupSearchRequest)
    test_vulnerability(
        "Path Traversal in search_id (/api/v1/search/setup)",
        "/api/v1/search/setup",
        {
            "search_id": "../../traversal_test",
            "brief_notes": "test",
            "jd_content": "test"
        }
    )

    # 4. Path Traversal in gem_id (RefineRequest)
    test_vulnerability(
        "Path Traversal in gem_id (/api/v1/gems/refine)",
        "/api/v1/gems/refine",
        {"gem_id": "../config", "instruction": "malicious edit"}
    )

    # 5. Information Leakage (Triggering an error)
    print("--- Testing: Information Leakage ---")
    # Trigger an error by providing an invalid local_dir that doesn't exist
    response = client.post("/api/v1/run", json={"search_id": "valid_id", "local_dir": "non_existent_dir"})
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
    detail = response.json().get("detail", "")
    if "runs/valid_id/outputs" in detail or "Traceback" in detail:
        print("❌ RESULT: VULNERABLE! Detailed path or internal info leaked in error message.")
    else:
        print("✅ RESULT: Generic or masked error message (safe).")
