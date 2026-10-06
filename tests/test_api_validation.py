import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH-123",
        local_dir="runs/SEARCH-123/inputs",
        candidate_id="CAND_1",
        webhook_url="https://api.example.com/webhook"
    )
    assert req.search_id == "SEARCH-123"
    assert req.local_dir == "runs/SEARCH-123/inputs"
    assert req.candidate_id == "CAND_1"
    assert req.webhook_url == "https://api.example.com/webhook"


def test_pipeline_request_invalid_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../../etc/passwd", local_dir="runs/inputs")
    assert "Identifier must contain only alphanumeric" in str(excinfo.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="SEARCH-1", candidate_id="../bad_candidate")
    assert "Identifier must contain only alphanumeric" in str(excinfo.value)


def test_pipeline_request_path_traversal_local_dir():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="SEARCH-1", local_dir="../secret_dir")
    assert "local_dir contains path traversal sequence" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="SEARCH-1", local_dir="/etc/passwd")
    assert "local_dir contains path traversal sequence" in str(excinfo.value)


def test_pipeline_request_ssrf_webhook_url():
    # Localhost / loopback checks
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="SEARCH-1", webhook_url="http://localhost:8000/hook")
    assert "webhook_url cannot point to localhost" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="SEARCH-1", webhook_url="http://127.0.0.1/hook")
    assert "webhook_url cannot point to localhost" in str(excinfo.value)

    # Private IP range
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="SEARCH-1", webhook_url="http://10.0.0.1/hook")
    assert "webhook_url points to a restricted IP address" in str(excinfo.value)

    # Invalid scheme
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="SEARCH-1", webhook_url="ftp://example.com/hook")
    assert "webhook_url must use http or https scheme" in str(excinfo.value)


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="SEARCH_001",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "SEARCH_001"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="SEARCH/../BAD",
            brief_notes="notes",
            jd_content="jd"
        )


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="Improve clarity")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="Improve clarity")
