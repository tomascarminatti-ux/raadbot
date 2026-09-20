import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_search_id_validation():
    # Valid search_ids
    req = PipelineRequest(search_id="valid_search-123")
    assert req.search_id == "valid_search-123"

    # Invalid search_ids with directory traversal / illegal chars
    invalid_ids = ["../secret", "search_id/path", "search_id; drop table", "search_id\n"]
    for inv in invalid_ids:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id=inv)

        with pytest.raises(ValidationError):
            SetupSearchRequest(search_id=inv, brief_notes="notes", jd_content="jd")


def test_candidate_id_validation():
    # Valid candidate_id
    req = PipelineRequest(search_id="s1", candidate_id="cand-123_abc")
    assert req.candidate_id == "cand-123_abc"

    # Invalid candidate_ids
    invalid_cands = ["../../etc/passwd", "cand/123", "cand\\123"]
    for inv in invalid_cands:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="s1", candidate_id=inv)


def test_gem_id_validation():
    # Valid gem_id
    req = RefineRequest(gem_id="gem1", instruction="make it better")
    assert req.gem_id == "gem1"

    # Invalid gem_ids trying path traversal to overwrite files outside prompts/
    invalid_gems = ["../config", "gem1/sub", "..\\config", "gem1\n"]
    for inv in invalid_gems:
        with pytest.raises(ValidationError):
            RefineRequest(gem_id=inv, instruction="test")


def test_local_dir_validation():
    # Valid local_dir
    req = PipelineRequest(search_id="s1", local_dir="data/inputs")
    assert req.local_dir == "data/inputs"

    # Invalid local_dirs (directory traversal or absolute paths)
    invalid_dirs = ["../runs", "data/../../etc", "/etc/passwd", "C:\\Windows"]
    for inv in invalid_dirs:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="s1", local_dir=inv)


def test_webhook_url_ssrf_validation():
    # Valid external webhooks
    req = PipelineRequest(search_id="s1", webhook_url="https://hooks.slack.com/services/123")
    assert req.webhook_url == "https://hooks.slack.com/services/123"

    # Invalid webhooks (SSRF attempts targeting local/private networks)
    invalid_urls = [
        "http://localhost:8000/api",
        "http://127.0.0.1:8000/internal",
        "http://0.0.0.0/test",
        "http://169.254.169.254/latest/meta-data",  # Link local cloud metadata
        "http://10.0.0.1/admin",  # Private IPv4
        "http://192.168.1.1/router",  # Private IPv4
        "ftp://example.com/webhook",  # Non http/https
    ]
    for url in invalid_urls:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="s1", webhook_url=url)
