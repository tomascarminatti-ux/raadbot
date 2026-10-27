import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="inputs/search_123",
        candidate_id="cand_1",
        webhook_url="https://example.com/webhook",
    )
    assert req.search_id == "search_123"
    assert req.candidate_id == "cand_1"
    assert req.local_dir == "inputs/search_123"
    assert req.webhook_url == "https://example.com/webhook"


@pytest.mark.parametrize(
    "invalid_id",
    [
        "../search",
        "search/123",
        "search; rm -rf",
        "search\n",
        "../../etc/passwd",
    ],
)
def test_pipeline_request_invalid_search_id(invalid_id):
    with pytest.raises(ValidationError):
        PipelineRequest(search_id=invalid_id, local_dir="inputs/test")


@pytest.mark.parametrize(
    "invalid_id",
    [
        "../cand",
        "cand/1",
        "cand\n",
    ],
)
def test_pipeline_request_invalid_candidate_id(invalid_id):
    with pytest.raises(ValidationError):
        PipelineRequest(
            search_id="valid_search",
            candidate_id=invalid_id,
            local_dir="inputs/test",
        )


@pytest.mark.parametrize(
    "invalid_dir",
    [
        "../inputs",
        "inputs/../secret",
        "/etc/passwd",
        "C:\\Windows\\System32",
    ],
)
def test_pipeline_request_invalid_local_dir(invalid_dir):
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_search", local_dir=invalid_dir)


@pytest.mark.parametrize(
    "invalid_url",
    [
        "http://localhost/webhook",
        "http://localhost:8000/webhook",
        "http://127.0.0.1/webhook",
        "http://10.0.0.1/webhook",
        "http://172.16.0.1/webhook",
        "http://192.168.1.1/webhook",
        "http://169.254.169.254/latest/meta-data",
        "ftp://example.com/webhook",
        "file:///etc/passwd",
    ],
)
def test_pipeline_request_invalid_webhook_url(invalid_url):
    with pytest.raises(ValidationError):
        PipelineRequest(
            search_id="valid_search",
            local_dir="inputs/test",
            webhook_url=invalid_url,
        )


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="search_valid",
        brief_notes="notes",
        jd_content="jd",
    )
    assert req.search_id == "search_valid"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../invalid_search",
            brief_notes="notes",
            jd_content="jd",
        )


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="make it shorter")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../../prompts/secret", instruction="hack")
