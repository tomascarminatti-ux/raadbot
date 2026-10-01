import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH-123_abc",
        local_dir="valid/path",
        candidate_id="CAND_01",
        webhook_url="https://api.example.com/webhook",
    )
    assert req.search_id == "SEARCH-123_abc"
    assert req.local_dir == "valid/path"
    assert req.candidate_id == "CAND_01"
    assert req.webhook_url == "https://api.example.com/webhook"


def test_pipeline_request_invalid_search_id_path_traversal():
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(search_id="../../etc/passwd", local_dir="valid/path")
    assert "Identifier must contain only alphanumeric" in str(exc.value)


def test_pipeline_request_invalid_local_dir_traversal():
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(search_id="SEARCH-001", local_dir="../secret_dir")
    assert "Directory traversal" in str(exc.value)


def test_pipeline_request_invalid_local_dir_absolute():
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(search_id="SEARCH-001", local_dir="/etc/passwd")
    assert "Directory traversal" in str(exc.value)


def test_pipeline_request_ssrf_localhost():
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(
            search_id="SEARCH-001",
            local_dir="valid/path",
            webhook_url="http://localhost:8000/internal",
        )
    assert "Forbidden webhook URL" in str(exc.value)


def test_pipeline_request_ssrf_loopback():
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(
            search_id="SEARCH-001",
            local_dir="valid/path",
            webhook_url="http://127.0.0.1/webhook",
        )
    assert "restricted IP address" in str(exc.value)


def test_pipeline_request_ssrf_aws_metadata():
    with pytest.raises(ValidationError) as exc:
        PipelineRequest(
            search_id="SEARCH-001",
            local_dir="valid/path",
            webhook_url="http://169.254.169.254/latest/meta-data/",
        )
    assert "restricted IP address" in str(exc.value)


def test_setup_search_request_path_traversal():
    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../bad_dir",
            brief_notes="notes",
            jd_content="jd",
        )


def test_refine_request_path_traversal():
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../../../etc/passwd", instruction="test")
