import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="valid-search_123",
        local_dir="valid/dir_path",
        candidate_id="cand_1",
        webhook_url="https://hooks.example.com/webhook",
    )
    assert req.search_id == "valid-search_123"
    assert req.local_dir == "valid/dir_path"
    assert req.candidate_id == "cand_1"
    assert req.webhook_url == "https://hooks.example.com/webhook"


def test_pipeline_request_path_traversal_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="../etc/passwd",
            local_dir="valid/path",
        )
    assert "Invalid identifier format" in str(excinfo.value)


def test_pipeline_request_path_traversal_candidate_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(
            search_id="valid_search",
            candidate_id="../../admin",
            local_dir="valid/path",
        )
    assert "Invalid identifier format" in str(excinfo.value)


def test_pipeline_request_path_traversal_local_dir():
    invalid_dirs = [
        "../secret",
        "folder/../../secret",
        "/absolute/path",
        "..\\windows\\system32",
    ]
    for d in invalid_dirs:
        with pytest.raises(ValidationError) as excinfo:
            PipelineRequest(
                search_id="valid_search",
                local_dir=d,
            )
        assert "Invalid directory path" in str(excinfo.value)


def test_pipeline_request_ssrf_webhook_url():
    invalid_urls = [
        "http://localhost/webhook",
        "http://127.0.0.1/webhook",
        "http://10.0.0.1/webhook",
        "http://192.168.1.1/webhook",
        "ftp://example.com/webhook",
    ]
    for url in invalid_urls:
        with pytest.raises(ValidationError) as excinfo:
            PipelineRequest(
                search_id="valid_search",
                local_dir="valid_dir",
                webhook_url=url,
            )
        assert "Invalid webhook_url target" in str(excinfo.value) or "webhook_url cannot target internal IPs" in str(excinfo.value)


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="search_101",
        brief_notes="notes",
        jd_content="content",
    )
    assert req.search_id == "search_101"

    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="search/../101",
            brief_notes="notes",
            jd_content="content",
        )
    assert "Invalid search_id format" in str(excinfo.value)


def test_refine_request_validation():
    req = RefineRequest(
        gem_id="gem1",
        instruction="Make it stricter",
    )
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(
            gem_id="../gem1",
            instruction="Make it stricter",
        )
    assert "Invalid gem_id format" in str(excinfo.value)
