import pytest
from pydantic import ValidationError
from api import PipelineRequest, RefineRequest, SetupSearchRequest
import config

def test_pipeline_request_validation():
    # Valid search_id
    req = PipelineRequest(search_id="valid_id_123")
    assert req.search_id == "valid_id_123"

    # Invalid search_id (path traversal)
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="../invalid")

    # Invalid search_id (special characters)
    with pytest.raises(ValidationError):
        PipelineRequest(search_id="id with spaces")

def test_refine_request_validation():
    # Valid gem_id
    req = RefineRequest(gem_id="gem1", instruction="test")
    assert req.gem_id == "gem1"

    # Invalid gem_id (path traversal)
    with pytest.raises(ValidationError):
        RefineRequest(gem_id="../../etc/passwd", instruction="test")

def test_setup_search_request_validation():
    # Valid
    req = SetupSearchRequest(search_id="valid", brief_notes="notes", jd_content="jd")
    assert req.search_id == "valid"

    # Invalid
    with pytest.raises(ValidationError):
        SetupSearchRequest(search_id="invalid/path", brief_notes="notes", jd_content="jd")

def test_allowed_gems_config():
    assert "gem1" in config.ALLOWED_GEMS
    assert "gem6" in config.ALLOWED_GEMS
    assert "../config" not in config.ALLOWED_GEMS
