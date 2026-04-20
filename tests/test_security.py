import os
from fastapi.testclient import TestClient
from api import app
from unittest.mock import patch

client = TestClient(app)


def test_path_traversal_search_id():
    # Attempt to use search_id for path traversal
    # Should now return 422 because of Pydantic validation
    response = client.post("/api/v1/run", json={
        "search_id": "../malicious",
        "local_dir": "tests"
    })
    print(f"Status Code for search_id traversal: {response.status_code}")
    assert response.status_code == 422
    assert not os.path.exists("malicious")


def test_path_traversal_local_dir():
    # Absolute path
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "/etc"
    })
    print(f"Status Code for local_dir absolute path: {response.status_code}")
    assert response.status_code == 422

    # Traversal
    response = client.post("/api/v1/run", json={
        "search_id": "test_search",
        "local_dir": "../../etc"
    })
    print(f"Status Code for local_dir traversal: {response.status_code}")
    assert response.status_code == 422


def test_path_traversal_refine_gem():
    response = client.post("/api/v1/gems/refine", json={
        "gem_id": "../config",
        "instruction": "make it better"
    })
    print(f"Status Code for gem_id traversal: {response.status_code}")
    # Should be 422 due to regex validation
    assert response.status_code == 422


def test_valid_requests():
    # Mock GeminiClient to avoid connection errors
    with patch("api.GeminiClient") as mock_gemini:
        mock_instance = mock_gemini.return_value
        mock_instance.run_gem.return_value = {
            "data": {"mandate_summary": "ok"}, "markdown": "ok"}

        response = client.post("/api/v1/search/setup", json={
            "search_id": "valid_search_123",
            "brief_notes": "notes",
            "jd_content": "jd"
        })
        print(f"Status Code for valid request: {response.status_code}")
        assert response.status_code == 200


if __name__ == "__main__":
    import sys
    # Manual run
    errors = 0
    try:
        test_path_traversal_search_id()
        print("✅ Search ID traversal blocked with 422")
    except Exception as e:
        print(
            f"❌ Search ID traversal test failed: {str(e) or 'Assertion Error'}")
        errors += 1

    try:
        test_path_traversal_local_dir()
        print("✅ Local dir traversal blocked with 422")
    except Exception as e:
        print(
            f"❌ Local dir traversal test failed: {str(e) or 'Assertion Error'}")
        errors += 1

    try:
        test_path_traversal_refine_gem()
        print("✅ Refine gem traversal blocked with 422")
    except Exception as e:
        print(
            f"❌ Refine gem traversal test failed: {str(e) or 'Assertion Error'}")
        errors += 1

    try:
        test_valid_requests()
        print("✅ Valid request passed validation")
    except Exception as e:
        print(
            f"❌ Valid request failed validation: {str(e) or 'Assertion Error'}")
        errors += 1

    if errors > 0:
        sys.exit(1)
