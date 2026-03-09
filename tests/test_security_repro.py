import pytest
from fastapi.testclient import TestClient
import os

# Mock config before importing app
os.environ["GEMINI_API_KEY"] = "fake_key"
os.environ["LLM_PROVIDER"] = "gemini"

from api import app

client = TestClient(app)

def test_error_hardening_run():
    # PipelineRequest valid but fails due to fake key (Internal Server Error)
    response = client.post("/api/v1/run", json={
        "search_id": "valid-search",
        "local_dir": "runs"
    })
    print(f"Response status (error hardening run): {response.status_code}")
    print(f"Response body (error hardening run): {response.json()}")
    # Before it was 400 and detail was the Gemini error.
    # Now it should be 500 and generic message.
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error during pipeline execution."

def test_error_hardening_refine():
    # Refine valid gem but fails due to fake key
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "gem1",
        "instruction": "make it better"
    })
    print(f"Response status (error hardening refine): {response.status_code}")
    print(f"Response body (error hardening refine): {response.json()}")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred during GEM refinement."

def test_business_validation_error():
    # Test that ValueError (business validation) still shows the message
    # In run_pipeline: if not request.drive_folder and not request.local_dir: raise ValueError(...)
    response = client.post("/api/v1/run", json={
        "search_id": "valid-search"
    })
    print(f"Response status (business validation): {response.status_code}")
    print(f"Response body (business validation): {response.json()}")
    assert response.status_code == 400
    assert "Se debe proveer 'drive_folder' o 'local_dir'" in response.json()["detail"]

if __name__ == "__main__":
    test_error_hardening_run()
    test_error_hardening_refine()
    test_business_validation_error()
