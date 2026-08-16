import pytest
from pydantic import ValidationError
from api import RefineRequest


def test_refine_request_valid_gem_id():
    req = RefineRequest(gem_id="gem1", instruction="Make prompt concise")
    assert req.gem_id == "gem1"

    req_dash = RefineRequest(gem_id="gem-1_v2", instruction="Update")
    assert req_dash.gem_id == "gem-1_v2"


def test_refine_request_path_traversal_prevention():
    invalid_gem_ids = [
        "../config",
        "gem1/../gem2",
        "../../etc/passwd",
        "gem1/../../secret",
        r"gem1\..",
        "gem1.md",
        "gem1*",
        "gem1;rm -rf",
    ]

    for invalid_id in invalid_gem_ids:
        with pytest.raises(ValidationError) as exc_info:
            RefineRequest(gem_id=invalid_id, instruction="Attempt exploit")
        assert "Invalid gem_id format" in str(exc_info.value)
