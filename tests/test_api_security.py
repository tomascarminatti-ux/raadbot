import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="data/runs",
        candidate_id="cand_1",
        webhook_url="https://example.com/webhook",
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "data/runs"


def test_pipeline_request_path_traversal():
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(search_id="../invalid")
    assert "Must contain only alphanumeric" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        PipelineRequest(search_id="valid_id", local_dir="../secret_dir")
    assert "Directory traversal not allowed" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        PipelineRequest(search_id="valid_id", candidate_id="../../cand")
    assert "Must contain only alphanumeric" in str(exc.value)


def test_pipeline_request_ssrf():
    # Localhost
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(search_id="valid_id", webhook_url="http://localhost:8000/webhook")
    assert "Localhost access blocked" in str(exc.value)

    # Loopback IP
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(search_id="valid_id", webhook_url="http://127.0.0.1:8000/webhook")
    assert "Access to private/local IP blocked" in str(exc.value)

    # AWS Metadata IP
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(search_id="valid_id", webhook_url="http://169.254.169.254/latest/meta-data")
    assert "Access to private/local IP blocked" in str(exc.value)


def test_setup_search_security():
    with pytest.raises(ValidationError) as exc:
        SetupSearchRequest(search_id="../bad_search", brief_notes="a", jd_content="b")
    assert "Must contain only alphanumeric" in str(exc.value)


def test_refine_request_security():
    with pytest.raises(ValidationError) as exc:
        RefineRequest(gem_id="../../etc/passwd", instruction="refine prompt")
    assert "Must contain only alphanumeric" in str(exc.value)
