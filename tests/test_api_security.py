import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_valid_pipeline_request():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="runs/input",
        candidate_id="cand-001",
        webhook_url="https://hooks.slack.com/services/test"
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "runs/input"
    assert req.candidate_id == "cand-001"


def test_invalid_search_id_path_traversal():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../etc/passwd", local_dir="valid/dir")


def test_invalid_search_id_newline():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search_123\n", local_dir="valid/dir")


def test_invalid_candidate_id():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search1", candidate_id="cand/../../")


def test_invalid_local_dir_traversal():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search1", local_dir="../secret_data")


def test_invalid_local_dir_absolute():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="search1", local_dir="/etc/shadow")


def test_invalid_webhook_ssrf_localhost():
    with pytest.raises(ValidationError):
        PipelineRequest(
            search_id="search1",
            local_dir="valid/dir",
            webhook_url="http://localhost:8000/internal"
        )


def test_invalid_webhook_ssrf_private_ip():
    with pytest.raises(ValidationError):
        PipelineRequest(
            search_id="search1",
            local_dir="valid/dir",
            webhook_url="http://192.168.1.1/admin"
        )


def test_invalid_webhook_ssrf_loopback():
    with pytest.raises(ValidationError):
        PipelineRequest(
            search_id="search1",
            local_dir="valid/dir",
            webhook_url="http://127.0.0.1/status"
        )


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="search-100",
        brief_notes="notes",
        jd_content="jd"
    )
    assert req.search_id == "search-100"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="search/../traversal",
            brief_notes="notes",
            jd_content="jd"
        )


def test_refine_request_validation():
    req = RefineRequest(gem_id="gem1", instruction="refine this")
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(
            gem_id="gem1; cat /etc/passwd",
            instruction="refine this"
        )
