import pytest
from pydantic import ValidationError
import os

# Set environment variables needed for api import
os.environ["GEMINI_API_KEY"] = "mock_key"

from api import PipelineRequest, SetupSearchRequest, RefineRequest

def test_pipeline_request_path_traversal():
    # Test search_id traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="/etc/passwd", local_dir="some/dir")

    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../secrets", local_dir="some/dir")

    # Test candidate_id traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", candidate_id="/etc/passwd", local_dir="some/dir")

    # Test valid input
    req = PipelineRequest(search_id="SEARCH-001", candidate_id="CAND-001", local_dir="some/dir")
    assert req.search_id == "SEARCH-001"
    assert req.candidate_id == "CAND-001"

def test_setup_search_request_path_traversal():
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="/etc/passwd", brief_notes="notes", jd_content="jd")

    req = SetupSearchRequest(search_id="VALID_ID", brief_notes="notes", jd_content="jd")
    assert req.search_id == "VALID_ID"

def test_refine_request_path_traversal():
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../gem1", instruction="refine")

    req = RefineRequest(gem_id="gem1", instruction="refine")
    assert req.gem_id == "gem1"
