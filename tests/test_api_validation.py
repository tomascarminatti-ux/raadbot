import pytest
from pydantic import ValidationError
from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_pipeline_request_valid():
    req = PipelineRequest(
        search_id="SEARCH_001",
        local_dir="data/search_001",
        candidate_id="candidate_A",
        webhook_url="https://api.example.com/webhook"
    )
    assert req.search_id == "SEARCH_001"
    assert req.local_dir == "data/search_001"
    assert req.candidate_id == "candidate_A"
    assert req.webhook_url == "https://api.example.com/webhook"


def test_pipeline_request_invalid_identifiers():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../etc/passwd", local_dir="data/test")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="SEARCH_001", candidate_id="../../candidate_1", local_dir="data/test")


def test_pipeline_request_invalid_local_dir():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="SEARCH_001", local_dir="../secret_dir")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="SEARCH_001", local_dir="/etc/passwd")


def test_pipeline_request_invalid_webhook_url():
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="SEARCH_001", local_dir="data", webhook_url="ftp://example.com/hook")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="SEARCH_001", local_dir="data", webhook_url="http://localhost:8000/hook")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="SEARCH_001", local_dir="data", webhook_url="http://127.0.0.1/hook")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="SEARCH_001", local_dir="data", webhook_url="http://10.0.0.1/hook")


def test_setup_search_request_validation():
    req = SetupSearchRequest(
        search_id="SEARCH-101",
        brief_notes="Notes",
        jd_content="JD Content"
    )
    assert req.search_id == "SEARCH-101"

    with pytest.raises(ValidationError):
        SetupSearchRequest(
            search_id="../invalid_id",
            brief_notes="Notes",
            jd_content="JD Content"
        )


def test_refine_request_validation():
    req = RefineRequest(
        gem_id="gem1",
        instruction="Make it strictly structured"
    )
    assert req.gem_id == "gem1"

    with pytest.raises(ValidationError):
        RefineRequest(
            gem_id="../gem1",
            instruction="Make it strictly structured"
        )
