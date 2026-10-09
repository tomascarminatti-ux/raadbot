import pytest
from pydantic import ValidationError
from api import RefineRequest


def test_refine_request_valid_gem_id():
    req = RefineRequest(gem_id="gem1", instruction="Make prompt more detailed")
    assert req.gem_id == "gem1"

    req_dash = RefineRequest(gem_id="gem_custom-2", instruction="Update instructions")
    assert req_dash.gem_id == "gem_custom-2"


def test_refine_request_path_traversal_rejected():
    invalid_ids = [
        "../gem1",
        "gem1/../../etc/passwd",
        "..\\gem1",
        "gem1\x00",
        "gem1.md",
        "gem 1",
        "gem1;cat /etc/passwd",
    ]

    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError) as exc_info:
            RefineRequest(gem_id=invalid_id, instruction="test instruction")
        assert "gem_id must contain only alphanumeric characters, underscores, or hyphens" in str(
            exc_info.value
        )
