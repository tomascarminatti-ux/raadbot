import os
import sys

from fastapi.testclient import TestClient

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app

client = TestClient(app)


def test_pipeline_request_path_traversal_on_search_id():
    """Verify that search_id rejects directory traversal and invalid characters."""
    bad_search_ids = [
        "../bad-dir",
        "..\\bad-dir",
        "search/id",
        "search_id$%",
        "nested/../path",
    ]
    for bid in bad_search_ids:
        response = client.post(
            "/api/v1/run", json={"search_id": bid, "local_dir": "runs/test"}
        )
        assert response.status_code == 422
        # Ensure it specifically references search_id or validation error
        assert "search_id" in response.text or "validation" in response.text


def test_pipeline_request_path_traversal_on_candidate_id():
    """Verify that candidate_id rejects directory traversal and invalid characters."""
    bad_candidate_ids = [
        "../bad-cand",
        "..\\bad-cand",
        "cand/id",
        "cand_id$%",
    ]
    for bid in bad_candidate_ids:
        response = client.post(
            "/api/v1/run",
            json={
                "search_id": "valid_search",
                "candidate_id": bid,
                "local_dir": "runs/test",
            },
        )
        assert response.status_code == 422
        assert "candidate_id" in response.text or "validation" in response.text


def test_pipeline_request_path_traversal_on_local_dir():
    """Verify that local_dir rejects directory traversal, absolute paths, and drive paths."""
    bad_local_dirs = [
        "../bad-dir",
        "..\\bad-dir",
        "/absolute/path",
        "C:\\absolute\\path",
        "nested/../../traversal",
        "dir:with:colons",
        "\\\\network\\share",
    ]
    for bdir in bad_local_dirs:
        response = client.post(
            "/api/v1/run", json={"search_id": "valid_search", "local_dir": bdir}
        )
        assert response.status_code == 422
        assert "local_dir" in response.text or "validation" in response.text


def test_setup_search_path_traversal_on_search_id():
    """Verify setup search rejects directory traversal in search_id."""
    bad_search_ids = [
        "../bad-dir",
        "..\\bad-dir",
        "search/id",
        "search_id$%",
    ]
    for bid in bad_search_ids:
        response = client.post(
            "/api/v1/search/setup",
            json={
                "search_id": bid,
                "brief_notes": "some notes",
                "jd_content": "some jd",
            },
        )
        assert response.status_code == 422
        assert "search_id" in response.text or "validation" in response.text


def test_refine_gem_path_traversal_on_gem_id():
    """Verify refine gem rejects directory traversal in gem_id."""
    bad_gem_ids = [
        "../bad-dir",
        "..\\bad-dir",
        "gem/id",
        "gem_id$%",
    ]
    for bid in bad_gem_ids:
        response = client.post(
            "/api/v1/gems/refine",
            json={
                "gem_id": bid,
                "instruction": "some instruction",
            },
        )
        assert response.status_code == 422
        assert "gem_id" in response.text or "validation" in response.text


def test_valid_inputs_accepted():
    """Verify that fully valid inputs are correctly parsed and not blocked by security validations."""
    response = client.post(
        "/api/v1/run",
        json={
            "search_id": "valid_search_123",
            "local_dir": "runs/test_gem6",  # valid relative path without traversal
            "candidate_id": "valid-cand_1",
        },
    )
    # Pydantic schema validation should pass, and either return 200 or 400 (or other downstream status), but NOT 422.
    assert response.status_code != 422
