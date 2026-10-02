import pytest
from pydantic import ValidationError
from api import RefineRequest


def test_refine_request_valid_gem_id():
    req = RefineRequest(gem_id="gem1", instruction="Improve quality")
    assert req.gem_id == "gem1"

    req2 = RefineRequest(gem_id="gem_5_test", instruction="Improve quality")
    assert req2.gem_id == "gem_5_test"


def test_refine_request_invalid_gem_id_path_traversal():
    invalid_ids = [
        "../gem1",
        "../../etc/passwd",
        "gem1/../gem2",
        "gem1\x00",
        "gem1.md",
        "gem1/gem2",
        "gem1\\gem2",
    ]

    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            RefineRequest(gem_id=invalid_id, instruction="Improve quality")
