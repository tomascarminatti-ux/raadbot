import pytest
from pydantic import ValidationError
from api import RefineRequest


def test_refine_request_valid_gem_id():
    req = RefineRequest(gem_id="gem1", instruction="Make it better")
    assert req.gem_id == "gem1"
    assert req.instruction == "Make it better"

    req_dash = RefineRequest(gem_id="gem_custom-1", instruction="Test")
    assert req_dash.gem_id == "gem_custom-1"


def test_refine_request_path_traversal_rejected():
    invalid_ids = [
        "../config",
        "../../etc/passwd",
        "gem1/../../secret",
        "gem1\x00",
        "gem1\n",
        "gem1; rm -rf /",
        "gem1.md",
        "gem 1",
    ]
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            RefineRequest(gem_id=invalid_id, instruction="Test instruction")
