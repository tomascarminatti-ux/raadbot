import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_valid_pipeline_request():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="data/search_1",
        candidate_id="cand-01",
        webhook_url="https://example.com/webhook"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "data/search_1"
    assert req.candidate_id == "cand-01"
    assert req.webhook_url == "https://example.com/webhook"


def test_invalid_search_id_path_traversal():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../etc/passwd")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search/123")


def test_invalid_local_dir_path_traversal():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="../secret")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="/etc/passwd")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="C:\\Windows")


def test_invalid_webhook_url_ssrf():
    # Localhost / Loopback
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", webhook_url="http://localhost:8000/callback")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", webhook_url="http://127.0.0.1:8000/callback")

    # Private IP range
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", webhook_url="http://10.0.0.1/callback")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", webhook_url="http://192.168.1.1/callback")

    # Non-http/https scheme
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", webhook_url="file:///etc/passwd")


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="search_abc",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "search_abc"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../invalid",
            brief_notes="notes",
            jd_content="jd"
        )


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="make it shorter")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="make it shorter")
