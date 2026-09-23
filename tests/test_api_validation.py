import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_2025_01",
        candidate_id="cand-101",
        local_dir="inputs/search1",
        webhook_url="https://n8n.example.com/webhook/123",
    )
    assert req.search_id == "search_2025_01"
    assert req.candidate_id == "cand-101"
    assert req.local_dir == "inputs/search1"
    assert req.webhook_url == "https://n8n.example.com/webhook/123"


def test_pipeline_request_path_traversal_search_id():
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(search_id="../runs/secret")
    assert "Identifier must contain only" in str(exc.value)


def test_pipeline_request_path_traversal_candidate_id():
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(
            search_id="valid_search",
            candidate_id="../../etc/passwd"
        )
    assert "Identifier must contain only" in str(exc.value)


def test_pipeline_request_path_traversal_local_dir():
    for bad_dir in ["../data", "/etc/data", "C:\\Windows\\System32"]:
        with pytest.raises(ValidationError) as exc:
            PipelineRequest(search_id="valid_search", local_dir=bad_dir)
        assert "Invalid local_dir path" in str(exc.value)


def test_pipeline_request_ssrf_webhook_url():
    bad_urls = [
        "http://localhost:8000/webhook",
        "http://127.0.0.1/webhook",
        "http://169.254.169.254/latest/meta-data/",
        "http://10.0.0.1/webhook",
        "ftp://example.com/webhook",
    ]
    for url in bad_urls:
        with pytest.raises(ValidationError) as exc:
            PipelineRequest(search_id="valid_search", webhook_url=url)
        assert ("webhook_url cannot target" in str(exc.value) or
                "must use http or https" in str(exc.value))


def test_setup_search_request_validation():
    # Valid
    req = SetupSearchRequest(
        search_id="search-001",
        brief_notes="notes",
        jd_content="jd",
    )
    assert req.search_id == "search-001"

    # Invalid search_id with path traversal
    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../bad_search",
            brief_notes="notes",
            jd_content="jd",
        )


def test_refine_request_validation():
    # Valid
    req = RefineRequest(gem_id="gem1", instruction="make it shorter")
    assert req.gem_id == "gem1"

    # Invalid gem_id with path traversal
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../../config", instruction="exploit")
