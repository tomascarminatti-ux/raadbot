import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH_001",
        candidate_id="CAND_123",
        local_dir="data/inputs",
        webhook_url="https://example.com/webhook",
    )
    assert req.search_id == "SEARCH_001"
    assert req.candidate_id == "CAND_123"
    assert req.local_dir == "data/inputs"
    assert req.webhook_url == "https://example.com/webhook"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../invalid/path")
    assert "search_id" in str(excinfo.value) or "ID must contain" in str(excinfo.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="VALID", candidate_id="../../cand")
    assert "candidate_id" in str(excinfo.value) or "ID must contain" in str(excinfo.value)


def test_pipeline_request_invalid_local_dir():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="VALID", local_dir="../secret_dir")
    assert "Invalid directory path" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="VALID", local_dir="/etc/passwd")
    assert "Invalid directory path" in str(excinfo.value)


def test_pipeline_request_ssrf_webhook_url():
    # Loopback IP / localhost
    for url in ["http://localhost:8000/hook", "http://127.0.0.1/hook", "http://[::1]/hook"]:
        with pytest.raises(ValidationError) as excinfo:
            PipelineRequest(search_id="VALID", webhook_url=url)
        assert "Webhook URL cannot target loopback addresses" in str(excinfo.value)

    # Private IP address
    for url in ["http://10.0.0.1/hook", "http://192.168.1.1/hook", "http://172.16.0.1/hook"]:
        with pytest.raises(ValidationError) as excinfo:
            PipelineRequest(search_id="VALID", webhook_url=url)
        assert "Webhook URL cannot target private IP addresses" in str(excinfo.value)

    # Invalid scheme
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="VALID", webhook_url="file:///etc/passwd")
    assert "Webhook URL must be a valid http or https URL" in str(excinfo.value)


def test_setup_search_request_validation():
    # Valid
    req = SetupSearchRequest(
        search_id="VALID_ID-123",
        brief_notes="notes",
        jd_content="jd",
    )
    assert req.search_id == "VALID_ID-123"

    # Invalid
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="../setup_path",
            brief_notes="notes",
            jd_content="jd",
        )
    assert "search_id" in str(excinfo.value)


def test_refine_request_validation():
    # Valid
    req = RefineRequest(gem_id="gem1", instruction="make concise")
    assert req.gem_id == "gem1"

    # Invalid path traversal
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="../gem1", instruction="make concise")
    assert "gem_id" in str(excinfo.value)
