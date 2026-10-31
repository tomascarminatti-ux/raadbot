import pytest
from pydantic import ValidationError

from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_valid_pipeline_request():
    req = PipelineRequest(
        search_id="SEARCH-123_abc",
        candidate_id="cand_01",
        local_dir="runs/SEARCH-123_abc/inputs",
        webhook_url="https://example.com/webhook",
    )
    assert req.search_id == "SEARCH-123_abc"
    assert req.candidate_id == "cand_01"
    assert req.local_dir == "runs/SEARCH-123_abc/inputs"
    assert req.webhook_url == "https://example.com/webhook"


def test_invalid_search_id_path_traversal():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../../etc/passwd", local_dir="inputs")
    assert "Identifier contains invalid characters" in str(exc_info.value)


def test_invalid_candidate_id_path_traversal():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="SEARCH-101", candidate_id="../secret_candidate"
        )
    assert "Identifier contains invalid characters" in str(exc_info.value)


def test_invalid_local_dir_path_traversal():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="SEARCH-101", local_dir="runs/../etc/passwd")
    assert "local_dir contains directory traversal" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="SEARCH-101", local_dir="/etc/passwd")
    assert "local_dir contains directory traversal" in str(exc_info.value)


def test_invalid_webhook_url_ssrf():
    loopback_urls = [
        "http://localhost:8000/callback",
        "http://127.0.0.1/callback",
        "http://[::1]/callback",
    ]
    for url in loopback_urls:
        with pytest.raises(ValidationError) as exc_info:
            PipelineRequest(search_id="SEARCH-101", webhook_url=url)
        assert "Webhook URL cannot target loopback addresses" in str(
            exc_info.value
        )

    private_urls = [
        "http://10.0.0.1/callback",
        "http://192.168.1.1/callback",
        "http://172.16.0.1/callback",
    ]
    for url in private_urls:
        with pytest.raises(ValidationError) as exc_info:
            PipelineRequest(search_id="SEARCH-101", webhook_url=url)
        assert "Webhook URL cannot target private IP addresses" in str(
            exc_info.value
        )

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="SEARCH-101", webhook_url="file:///etc/passwd"
        )
    assert "Webhook URL must be a valid http or https URL" in str(
        exc_info.value
    )


def test_setup_search_request_validation():
    valid = SetupSearchRequest(
        search_id="SEARCH-001", brief_notes="Notes", jd_content="JD"
    )
    assert valid.search_id == "SEARCH-001"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../SEARCH-001", brief_notes="Notes", jd_content="JD"
        )


def test_refine_request_validation():
    valid = RefineRequest(gem_id="gem1", instruction="Make prompt precise")
    assert valid.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="gem1/../../etc", instruction="Hack")
