import pytest
from pydantic import ValidationError
from api import RefineRequest


def test_refine_request_valid_gem_id():
    req = RefineRequest(gem_id="gem1", instruction="Improve clarity")
    assert req.gem_id == "gem1"

    req2 = RefineRequest(gem_id="gem_5_custom-v2", instruction="Add details")
    assert req2.gem_id == "gem_5_custom-v2"


def test_refine_request_path_traversal_rejection():
    invalid_ids = [
        "../gem1",
        "../../etc/passwd",
        "gem1/../gem2",
        "gem1\\..\\gem2",
        "gem1;rm -rf /",
        "gem 1",
        "gem1.md",
        "gem1/file",
        "/etc/passwd",
    ]

    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            RefineRequest(gem_id=invalid_id, instruction="Test instruction")
