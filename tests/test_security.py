import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_path_traversal():
    """Verify path traversal sequences in local_dir are rejected."""
    # Valid relative paths
    req = PipelineRequest(
        search_id="test-search",
        local_dir="runs/SEARCH-TEST-001/inputs"
    )
    assert req.local_dir == "runs/SEARCH-TEST-001/inputs"

    # Traversal attempts
    bad_paths = [
        "../secret",
        "runs/../../etc/passwd",
        "..\\secret",
        "/etc/passwd",
        "C:\\Windows"
    ]
    for bad_path in bad_paths:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="test-search", local_dir=bad_path)


def test_pipeline_request_ssrf():
    """Verify localhost, private IPs, non-http schemes are rejected."""
    # Valid external URL
    valid_url = "https://hooks.slack.com/services/abc/xyz"
    req = PipelineRequest(search_id="test-search", webhook_url=valid_url)
    assert req.webhook_url == valid_url

    # Blocked SSRF targets
    blocked_urls = [
        "http://localhost/hook",
        "http://127.0.0.1:8000/hook",
        "http://0.0.0.0/hook",
        "http://10.0.0.1/callback",
        "http://192.168.1.100/callback",
        "http://172.16.0.5/callback",
        "http://169.254.169.254/latest/meta-data/",
        "ftp://example.com/file",
        "javascript:alert(1)",
    ]
    for url in blocked_urls:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="test-search", webhook_url=url)


def test_safe_identifier_validation():
    """Verify identifiers allow only alphanumeric, dashes, and underscores."""
    # Valid identifiers
    p_req = PipelineRequest(
        search_id="SEARCH_2026-001",
        candidate_id="cand-001_A"
    )
    assert p_req.search_id == "SEARCH_2026-001"
    assert p_req.candidate_id == "cand-001_A"

    s_req = SetupSearchRequest(
        search_id="SEARCH-001",
        brief_notes="notes",
        jd_content="jd"
    )
    assert s_req.search_id == "SEARCH-001"

    r_req = RefineRequest(gem_id="gem1", instruction="make it concise")
    assert r_req.gem_id == "gem1"

    # Invalid identifiers
    invalid_ids = [
        "../../etc/passwd",
        "search; rm -rf",
        "search`id`",
        "search id",
        "search\nid",
    ]
    for bad_id in invalid_ids:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id=bad_id)
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="valid", candidate_id=bad_id)
        with pytest.raises(ValidationError):
            SetupSearchRequest(
                search_id=bad_id, brief_notes="n", jd_content="j"
            )
        with pytest.raises(ValidationError):
            RefineRequest(gem_id=bad_id, instruction="i")
