import pytest
from pydantic import ValidationError
from api import PipelineRequest


def test_pipeline_request_webhook_url_valid():
    request = PipelineRequest(
        search_id="test-search",
        local_dir="valid_dir",
        webhook_url="https://n8n.example.com/webhook/123",
    )
    assert request.webhook_url == "https://n8n.example.com/webhook/123"


def test_pipeline_request_webhook_url_none():
    request = PipelineRequest(
        search_id="test-search",
        local_dir="valid_dir",
        webhook_url=None,
    )
    assert request.webhook_url is None


def test_pipeline_request_webhook_url_invalid_scheme():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="test-search",
            local_dir="valid_dir",
            webhook_url="ftp://n8n.example.com/webhook",
        )
    assert "webhook_url scheme must be http or https" in str(
        exc_info.value
    )

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="test-search",
            local_dir="valid_dir",
            webhook_url="file:///etc/passwd",
        )
    assert "webhook_url scheme must be http or https" in str(
        exc_info.value
    )


def test_pipeline_request_webhook_url_restricted_localhost():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="test-search",
            local_dir="valid_dir",
            webhook_url="http://localhost:8000/webhook",
        )
    assert "webhook_url target is restricted (localhost)" in str(
        exc_info.value
    )


@pytest.mark.parametrize(
    "restricted_url",
    [
        "http://127.0.0.1/webhook",
        "http://127.0.0.1:8000/webhook",
        "http://10.0.0.1/webhook",
        "http://172.16.0.1/webhook",
        "http://192.168.1.1/webhook",
        "http://169.254.169.254/latest/meta-data/",
    ],
)
def test_pipeline_request_webhook_url_restricted_ips(restricted_url):
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(
            search_id="test-search",
            local_dir="valid_dir",
            webhook_url=restricted_url,
        )
    assert "webhook_url target is restricted (internal IP)" in str(
        exc_info.value
    )
