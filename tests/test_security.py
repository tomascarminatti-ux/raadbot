import pytest
from pydantic import ValidationError
from api import RefineRequest


def test_refine_request_gem_id_validation():
    """Verify that gem_id validation accepts valid inputs and blocks path traversal attempts."""
    # Valid gem_id inputs
    req1 = RefineRequest(gem_id="gem1", instruction="Improve prompt")
    assert req1.gem_id == "gem1"

    req2 = RefineRequest(gem_id="gem-5_test", instruction="Improve prompt")
    assert req2.gem_id == "gem-5_test"

    # Invalid gem_id inputs (path traversal & special chars)
    invalid_gem_ids = [
        "../gem1",
        "gem1/../../etc/passwd",
        "gem1.md",
        "gem1; id",
        "..\\config",
        "/etc/passwd",
    ]

    for invalid_id in invalid_gem_ids:
        with pytest.raises(ValidationError) as exc_info:
            RefineRequest(gem_id=invalid_id, instruction="Improve prompt")
        assert (
            "gem_id must contain only alphanumeric characters, hyphens, or underscores"
            in str(exc_info.value)
        )
