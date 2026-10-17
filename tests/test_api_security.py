import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="data/inputs",
        candidate_id="candidate-01",
        webhook_url="https://hooks.n8n.cloud/webhook/test"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "data/inputs"
    assert req.candidate_id == "candidate-01"
    assert req.webhook_url == "https://hooks.n8n.cloud/webhook/test"


def test_pipeline_request_path_traversal_search_id():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="../../etc/passwd", local_dir="data")
    assert "Invalid identifier format" in str(excinfo.value)


def test_pipeline_request_path_traversal_local_dir():
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", local_dir="../secret_dir")
    assert "Path traversal sequences are not allowed" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", local_dir="/etc/passwd")
    assert "Path traversal sequences are not allowed" in str(excinfo.value)


def test_pipeline_request_ssrf_webhook_url():
    # Test invalid scheme
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", webhook_url="ftp://example.com/hook")
    assert "webhook_url must use http or https scheme" in str(excinfo.value)

    # Test localhost
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", webhook_url="http://localhost:8000/webhook")
    assert "webhook_url cannot target localhost or loopback" in str(excinfo.value)

    # Test loopback IP
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", webhook_url="http://127.0.0.1/webhook")
    assert "webhook_url cannot target private or loopback IP addresses" in str(excinfo.value)

    # Test private IP
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", webhook_url="http://10.0.0.1/webhook")
    assert "webhook_url cannot target private or loopback IP addresses" in str(excinfo.value)

    # Test link-local IP
    with pytest.raises(ValidationError) as excinfo:
        PipelineRequest(search_id="search1", webhook_url="http://169.254.169.254/latest/meta-data")
    assert "webhook_url cannot target private or loopback IP addresses" in str(excinfo.value)


def test_setup_search_request_validation():
    # Valid request
    req = SetupSearchRequest(
        search_id="search_abc-123",
        brief_notes="notes",
        jd_content="jd content"
    )
    assert req.search_id == "search_abc-123"

    # Invalid search_id
    with pytest.raises(ValidationError) as excinfo:
        SetupSearchRequest(
            search_id="search/../id",
            brief_notes="notes",
            jd_content="jd content"
        )
    assert "Invalid identifier format" in str(excinfo.value)


def test_refine_request_validation():
    # Valid request
    req = RefineRequest(gem_id="gem1", instruction="Improve prompt")
    assert req.gem_id == "gem1"

    # Path traversal gem_id
    with pytest.raises(ValidationError) as excinfo:
        RefineRequest(gem_id="../config", instruction="Overwrite config")
    assert "Invalid identifier format" in str(excinfo.value)
