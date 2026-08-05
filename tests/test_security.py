import pytest
from unittest.mock import patch, MagicMock, mock_open
from fastapi.testclient import TestClient

# Import app from api
from api import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_api_dependencies():
    """Mock all external dependencies and file operations in api.py for safe testing."""
    # Mock prompt content for read operations
    m_open = mock_open(read_data="# Mock prompt content\n{{PROMPT_MAESTRO}}\n")

    with patch("api.run_pipeline") as mock_run_pipe, \
         patch("api.GeminiClient") as mock_gemini_cls, \
         patch("api.os.makedirs") as mock_makedirs, \
         patch("api.os.path.exists") as mock_exists, \
         patch("builtins.open", m_open):

        # Setup run_pipeline mock
        mock_run_pipe.return_value = {
            "status": "success",
            "search_id": "VALID-SEARCH-123",
            "output_dir": "runs/VALID-SEARCH-123/outputs",
            "summary": {}
        }

        # Setup GeminiClient mock
        mock_gemini_instance = MagicMock()
        mock_gemini_instance.run_gem.return_value = {
            "json": {"action": "finalize", "status": "SUCCESS"},
            "markdown": "mocked markdown content",
            "raw": "mocked raw content",
            "data": {"mandate_summary": "mocked summary"}
        }
        mock_gemini_cls.return_value = mock_gemini_instance

        # Setup os.path.exists mock to always return True
        mock_exists.return_value = True

        yield


def test_health_endpoint():
    """Verify health check endpoint works normally."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_run_pipeline_valid_search_id():
    """Test that valid search_id and candidate_id are correctly parsed by the Pydantic model."""
    payload = {
        "search_id": "VALID-SEARCH-123",
        "candidate_id": "CAND-001",
        "local_dir": "runs/test_gem6",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@pytest.mark.parametrize(
    "bad_search_id",
    [
        "../../etc/passwd",
        "..\\etc\\passwd",
        "search_id/with/slashes",
        "search_id\\with\\backslashes",
        "",
        "   ",
        "search_id_with_$",
    ],
)
def test_run_pipeline_invalid_search_id(bad_search_id):
    """Test that path traversal or illegal characters in search_id are caught by validation (returns 422)."""
    payload = {
        "search_id": bad_search_id,
        "candidate_id": "CAND-001",
        "local_dir": "runs/test_gem6",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text


@pytest.mark.parametrize(
    "bad_candidate_id",
    [
        "../../etc/passwd",
        "..\\etc\\passwd",
        "candidate/with/slashes",
        "candidate\\with\\backslashes",
        "",
        "   ",
        "candidate_with_$",
    ],
)
def test_run_pipeline_invalid_candidate_id(bad_candidate_id):
    """Test that path traversal or illegal characters in candidate_id are caught by validation (returns 422)."""
    payload = {
        "search_id": "VALID-SEARCH",
        "candidate_id": bad_candidate_id,
        "local_dir": "runs/test_gem6",
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "candidate_id" in response.text


@pytest.mark.parametrize(
    "bad_local_dir",
    [
        "../../etc",
        "..\\etc",
        "/etc",
        "C:\\Windows",
        "D:/Data",
    ],
)
def test_run_pipeline_invalid_local_dir(bad_local_dir):
    """Test that directory traversal or absolute paths in local_dir are rejected (returns 422)."""
    payload = {
        "search_id": "VALID-SEARCH",
        "candidate_id": "CAND-001",
        "local_dir": bad_local_dir,
    }
    response = client.post("/api/v1/run", json=payload)
    assert response.status_code == 422
    assert "local_dir" in response.text


@pytest.mark.parametrize(
    "bad_search_id",
    [
        "../../etc/passwd",
        "..\\etc\\passwd",
        "search_id/with/slashes",
        "search_id\\with\\backslashes",
        "",
        "   ",
    ],
)
def test_setup_search_invalid_search_id(bad_search_id):
    """Test that path traversal in setup search_id is caught by validation (returns 422)."""
    payload = {
        "search_id": bad_search_id,
        "brief_notes": "notes",
        "jd_content": "jd content",
    }
    response = client.post("/api/v1/search/setup", json=payload)
    assert response.status_code == 422
    assert "search_id" in response.text


@pytest.mark.parametrize(
    "bad_gem_id",
    [
        "../../README",
        "..\\README",
        "gem6",
        "gem10",
        "invalid_gem",
        "",
        "   ",
    ],
)
def test_refine_gem_invalid_gem_id(bad_gem_id):
    """Test that invalid or path traversal gem_id in refine is caught by validation (returns 422)."""
    payload = {
        "gem_id": bad_gem_id,
        "instruction": "Make it better",
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 422
    assert "gem_id" in response.text


@pytest.mark.parametrize(
    "valid_gem_id",
    [
        "gem1",
        "gem2",
        "gem3",
        "gem4",
        "gem5",
    ],
)
def test_refine_gem_valid_gem_id_parsing(valid_gem_id):
    """Test that valid gem_id passes validation."""
    payload = {
        "gem_id": valid_gem_id,
        "instruction": "Make it better",
    }
    response = client.post("/api/v1/gems/refine", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
