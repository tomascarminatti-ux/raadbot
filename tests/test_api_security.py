import pytest
from pydantic import ValidationError

from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH_001",
        candidate_id="CAND-123",
        local_dir="data/inputs_001",
        webhook_url="https://hooks.example.com/api/v1/callback",
    )
    assert req.search_id == "SEARCH_001"
    assert req.candidate_id == "CAND-123"
    assert req.local_dir == "data/inputs_001"
    assert req.webhook_url == "https://hooks.example.com/api/v1/callback"


def test_pipeline_request_invalid_search_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../../etc/passwd", local_dir="inputs")
    assert "Invalid identifier format" in str(exc_info.value)


def test_pipeline_request_invalid_candidate_id():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="SEARCH1",
            candidate_id="../cand1",
            local_dir="inputs",
        )
    assert "Invalid identifier format" in str(exc_info.value)


def test_pipeline_request_path_traversal_local_dir():
    invalid_dirs = [
        "../secret_dir",
        "folder/../../etc",
        "/absolute/path",
        "C:\\Windows\\System32",
    ]
    for d in invalid_dirs:
        with pytest.raises(ValidationError) as exc_info:
            PipelineRequest(search_id="SEARCH1", local_dir=d)
        assert "Directory traversal not allowed" in str(exc_info.value)


def test_pipeline_request_ssrf_webhook_url():
    invalid_urls = [
        "http://localhost/webhook",
        "http://127.0.0.1/webhook",
        "http://10.0.0.1/webhook",
        "http://172.16.0.1/webhook",
        "http://192.168.1.1/webhook",
        "http://169.254.169.254/latest/meta-data",
        "ftp://example.com/webhook",
        "file:///etc/passwd",
    ]
    for url in invalid_urls:
        with pytest.raises(ValidationError):
            PipelineRequest(
                search_id="SEARCH1",
                local_dir="inputs",
                webhook_url=url,
            )


def test_setup_search_request_validation():
    valid = SetupSearchRequest(
        search_id="SEARCH-99",
        brief_notes="notes",
        jd_content="jd",
    )
    assert valid.search_id == "SEARCH-99"

    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="SEARCH/99",
            brief_notes="notes",
            jd_content="jd",
        )
    assert "Invalid identifier format" in str(exc_info.value)


def test_refine_request_validation():
    valid = RefineRequest(gem_id="gem1", instruction="make it clearer")
    assert valid.gem_id == "gem1"

    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(gem_id="../gem1", instruction="hack")
    assert "Invalid identifier format" in str(exc_info.value)
