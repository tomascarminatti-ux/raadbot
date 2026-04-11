
import pytest
from pydantic import ValidationError
import os

# Set dummy environment variable for config.py
os.environ["GEMINI_API_KEY"] = "dummy_key"

from api import PipelineRequest, SetupSearchRequest, RefineRequest

def test_pipeline_request_path_traversal():
    # search_id traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../evil", local_dir="test")

    # local_dir absolute path
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="/etc/passwd")

    # local_dir traversal
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid_id", local_dir="tests/../../")

def test_setup_search_request_path_traversal():
    # search_id traversal
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="../../root", brief_notes="test", jd_content="test")

def test_refine_request_path_traversal():
    # gem_id traversal
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../config", instruction="test")

    # gem_id absolute path
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="/etc/passwd", instruction="test")

def test_candidate_id_path_traversal():
    # candidate_id traversal in PipelineRequest
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="valid", local_dir="test", candidate_id="../attacker")
