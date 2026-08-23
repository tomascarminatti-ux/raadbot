import pytest
from pydantic import ValidationError

from api import PipelineRequest, SetupSearchRequest, RefineRequest


def test_valid_pipeline_request():
    req = PipelineRequest(
        search_id="search_123",
        local_dir="data/search_123",
        candidate_id="cand_abc-1",
    )
    assert req.search_id == "search_123"
    assert req.local_dir == "data/search_123"
    assert req.candidate_id == "cand_abc-1"


def test_invalid_identifiers():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="../invalid_id")
    assert "search_id" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid", candidate_id="cand/../../etc")
    assert "candidate_id" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        SetupSearchRequest(
            search_id="search/id",
            brief_notes="brief",
            jd_content="jd",
        )
    assert "search_id" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        RefineRequest(gem_id="gem1; rm -rf /", instruction="refine")
    assert "gem_id" in str(exc_info.value)


def test_path_traversal_local_dir():
    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", local_dir="../etc/passwd")
    assert "local_dir" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", local_dir="data/../secret")
    assert "local_dir" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        PipelineRequest(search_id="valid_search", local_dir="/etc/passwd")
    assert "local_dir" in str(exc_info.value)
