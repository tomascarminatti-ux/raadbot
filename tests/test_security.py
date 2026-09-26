import pytest
from pydantic import ValidationError

from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_valid_pipeline_request():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="inputs/search_123",
        candidate_id="candidate_abc",
        webhook_url="https://example.com/webhook"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "inputs/search_123"
    assert req.candidate_id == "candidate_abc"
    assert req.webhook_url == "https://example.com/webhook"


@pytest.mark.parametrize("invalid_id", [
    "../etc/passwd",
    "search_123\n",
    "search/123",
    "search id",
    "search_123;",
])
def test_pipeline_request_invalid_search_id(invalid_id):
    with pytest.raises(ValidationError):
        PipelineRequest(search_id=invalid_id, local_dir="inputs/valid")


@pytest.mark.parametrize("invalid_path", [
    "../inputs",
    "inputs/../secret",
    "/etc/passwd",
    "C:\\Windows\\System32",
    "inputs\\..\\secret"
])
def test_pipeline_request_invalid_local_dir(invalid_path):
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search_123", local_dir=invalid_path)


@pytest.mark.parametrize("ssrf_url", [
    "http://localhost/webhook",
    "http://localhost:8000/webhook",
    "http://127.0.0.1/webhook",
    "http://0.0.0.0/webhook",
    "http://169.254.169.254/latest/meta-data/",
    "http://10.0.0.1/webhook",
    "http://172.16.0.1/webhook",
    "http://192.168.1.1/webhook",
    "ftp://example.com/webhook",
    "file:///etc/passwd",
])
def test_pipeline_request_ssrf_webhook(ssrf_url):
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search_123", webhook_url=ssrf_url)


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="search_456",
        brief_notes="test brief",
        jd_content="test jd"
    )
    assert req.search_id == "search_456"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../bad_search",
            brief_notes="test brief",
            jd_content="test jd"
        )


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="Refine prompt")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="Refine prompt")
