import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_001",
        candidate_id="cand-123",
        local_dir="data/inputs",
        webhook_url="https://hooks.slack.com/services/test/webhook"
    )
    assert req.search_id == "search_001"
    assert req.candidate_id == "cand-123"
    assert req.local_dir == "data/inputs"
    assert req.webhook_url == "https://hooks.slack.com/services/test/webhook"


def test_pipeline_request_invalid_identifiers():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../invalid_search")
    assert "Identifier must contain only" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="search_1", candidate_id="cand/../bad")
    assert "Identifier must contain only" in str(exc_info.value)


def test_pipeline_request_invalid_local_dir():
    invalid_dirs = [
        "../etc/passwd",
        "inputs/../secret",
        "/absolute/path",
        r"C:\Windows\System32",
    ]
    for d in invalid_dirs:
        with pytest.raises(ValidationError) as exc_info:
            PipelineRequest(search_id="search1", local_dir=d)
        assert "Invalid local_dir path" in str(exc_info.value)


def test_pipeline_request_ssrf_webhook_urls():
    invalid_urls = [
        "http://localhost:8000/webhook",
        "http://127.0.0.1/callback",
        "http://10.0.0.1/internal",
        "http://192.168.1.1/admin",
        "http://169.254.169.254/latest/meta-data/",
        "file:///etc/passwd",
        "ftp://example.com/file",
    ]
    for url in invalid_urls:
        with pytest.raises(ValidationError) as exc_info:
            PipelineRequest(search_id="search1", webhook_url=url)
        assert "Invalid webhook URL" in str(exc_info.value) or "restricted IP address" in str(exc_info.value)


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="valid_search-123",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "valid_search-123"

    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="../../bad_search",
            brief_notes="notes",
            jd_content="jd"
        )
    assert "search_id must contain only" in str(exc_info.value)


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="Improve clarity")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(gem_id="../gem1", instruction="Hack prompt")
    assert "gem_id must contain only" in str(exc_info.value)
