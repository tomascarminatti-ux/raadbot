import pytest
from pydantic import ValidationError
from api import RefineRequest


def test_refine_request_valid_gem_id():
    valid_ids = ["gem1", "gem_5", "gem-1", "GEM10", "custom_gem_v2"]
    for gem_id in valid_ids:
        req = RefineRequest(gem_id=gem_id, instruction="Make it concise")
        assert req.gem_id == gem_id


def test_refine_request_invalid_gem_id_path_traversal():
    invalid_ids = [
        "../gem1",
        "../../etc/passwd",
        "gem1/extra",
        "gem1\\extra",
        "gem1;rm -rf /",
        "gem1.md",
        "gem 1",
        "gem1\n",
    ]
    for gem_id in invalid_ids:
        with pytest.raises(ValidationError) as exc_info:
            RefineRequest(gem_id=gem_id, instruction="Make it concise")
        assert "gem_id must contain only alphanumeric characters" in str(exc_info.value)
