import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="inputs/search_123",
        candidate_id="cand-001",
        webhook_url="https://hooks.n8n.example.com/webhook/123",
    )
    assert req.search_id == "search_123"
    assert req.candidate_id == "cand-001"
    assert req.local_dir == "inputs/search_123"
    assert req.webhook_url == "https://hooks.n8n.example.com/webhook/123"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="../etc/passwd",
            local_dir="inputs/test",
        )
    assert "search_id must contain only alphanumeric characters" in str(exc_info.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="inputs/test",
            candidate_id="cand/../../etc",
        )
    assert "candidate_id must contain only alphanumeric characters" in str(exc_info.value)


def test_pipeline_request_path_traversal_local_dir():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="../../etc/passwd",
        )
    assert "local_dir must be a relative path without directory traversal" in str(exc_info.value)


def test_pipeline_request_ssrf_webhook_url_loopback():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="inputs/test",
            webhook_url="http://127.0.0.1:8000/internal",
        )
    assert "webhook_url cannot target private or loopback IP addresses" in str(exc_info.value)


def test_pipeline_request_ssrf_webhook_url_localhost():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="inputs/test",
            webhook_url="http://localhost:8000/internal",
        )
    assert "webhook_url cannot target localhost" in str(exc_info.value)


def test_pipeline_request_ssrf_webhook_url_metadata():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="valid_search",
            local_dir="inputs/test",
            webhook_url="http://169.254.169.254/latest/meta-data/",
        )
    assert "webhook_url cannot target private or loopback IP addresses" in str(exc_info.value)


def test_setup_search_request_invalid_search_id():
    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="search/../traversal",
            brief_notes="notes",
            jd_content="jd",
        )
    assert "search_id must contain only alphanumeric characters" in str(exc_info.value)


def test_refine_request_invalid_gem_id():
    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(
            gem_id="../gem1",
            instruction="refine prompt",
        )
    assert "gem_id must contain only alphanumeric characters" in str(exc_info.value)
