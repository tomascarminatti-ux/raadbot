import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="data/inputs",
        candidate_id="cand-01",
        webhook_url="https://example.com/webhook",
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "data/inputs"
    assert req.candidate_id == "cand-01"
    assert req.webhook_url == "https://example.com/webhook"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../etc/passwd", local_dir="data")
    assert "search_id" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="search;id", local_dir="data")
    assert "search_id" in str(exc_info.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", candidate_id="cand/../../etc")
    assert "candidate_id" in str(exc_info.value)


def test_pipeline_request_invalid_local_dir_traversal():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", local_dir="../secret")
    assert "local_dir" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", local_dir="/etc/passwd")
    assert "local_dir" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", local_dir="C:\\Windows\\System32")
    assert "local_dir" in str(exc_info.value)


def test_pipeline_request_ssrf_webhook_url():
    # Disallowed non-http/https schemes
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", webhook_url="file:///etc/passwd")
    assert "webhook_url" in str(exc_info.value)

    # Disallowed localhost
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", webhook_url="http://localhost/callback")
    assert "webhook_url" in str(exc_info.value)

    # Disallowed loopback IP
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", webhook_url="http://127.0.0.1:8000/callback")
    assert "webhook_url" in str(exc_info.value)

    # Disallowed private IP
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", webhook_url="http://192.168.1.1/callback")
    assert "webhook_url" in str(exc_info.value)

    # Disallowed AWS metadata endpoint
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", webhook_url="http://169.254.169.254/latest/meta-data/")
    assert "webhook_url" in str(exc_info.value)


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="search_abc-123",
        brief_notes="notes",
        jd_content="jd",
    )
    assert req.search_id == "search_abc-123"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="search/traversal",
            brief_notes="notes",
            jd_content="jd",
        )


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="make concise")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../../prompts/gem1", instruction="hack")
