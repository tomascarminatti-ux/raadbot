import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_path_traversal_search_id():
    invalid_ids = ["../search", "../../etc/passwd", "search/id", "search id", "search_id\n"]
    for bad_id in invalid_ids:
        with pytest.raises(ValidationError) as exc_info:
            PipelineRequest(search_id=bad_id)
        assert "search_id" in str(exc_info.value) or "Identifier" in str(exc_info.value)


def test_pipeline_request_path_traversal_candidate_id():
    invalid_candidate_ids = ["../cand", "cand/../../secret", "cand id"]
    for bad_id in invalid_candidate_ids:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="search_001", candidate_id=bad_id)


def test_pipeline_request_path_traversal_local_dir():
    invalid_dirs = ["../../etc", "/etc/passwd", "C:\\Windows", "inputs/../secret", "inputs/.."]
    for bad_dir in invalid_dirs:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="search_001", local_dir=bad_dir)


def test_pipeline_request_ssrf_webhook_url():
    invalid_urls = [
        "http://localhost/hook",
        "http://localhost:8000/hook",
        "http://127.0.0.1/hook",
        "http://127.0.0.1:8000/hook",
        "http://169.254.169.254/latest/meta-data/",
        "http://10.0.0.1/hook",
        "http://192.168.1.1/hook",
        "ftp://example.com/hook",
        "invalid_url",
    ]
    for url in invalid_urls:
        with pytest.raises(ValidationError):
            PipelineRequest(search_id="search_001", webhook_url=url)


def test_pipeline_request_valid_inputs():
    req = PipelineRequest(
        search_id="search_001",
        local_dir="inputs/search_01",
        candidate_id="cand_123",
        webhook_url="https://n8n.example.com/webhook/123",
    )
    assert req.search_id == "search_001"
    assert req.local_dir == "inputs/search_01"
    assert req.candidate_id == "cand_123"
    assert req.webhook_url == "https://n8n.example.com/webhook/123"


def test_setup_search_request_validation():
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="../invalid", brief_notes="notes", jd_content="jd")

    req = SetupSearchRequest(search_id="search_001", brief_notes="notes", jd_content="jd")
    assert req.search_id == "search_001"


def test_refine_request_validation():
    invalid_gem_ids = ["../config", "gem1/../../secret", "gem 1", "gem1\n"]
    for bad_gem_id in invalid_gem_ids:
        with pytest.raises(ValidationError):
            RefineRequest(gem_id=bad_gem_id, instruction="Make it shorter")

    req = RefineRequest(gem_id="gem1", instruction="Make it shorter")
    assert req.gem_id == "gem1"
