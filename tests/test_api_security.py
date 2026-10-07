import pytest
from pydantic import ValidationError
from api import SetupSearchRequest


def test_setup_search_request_valid():
    """Verify SetupSearchRequest accepts valid search_ids."""
    req = SetupSearchRequest(
        search_id="search_123-abc",
        brief_notes="Notes",
        jd_content="JD text",
    )
    assert req.search_id == "search_123-abc"


def test_setup_search_request_path_traversal_invalid():
    """Verify SetupSearchRequest rejects path traversal or invalid characters in search_id."""
    invalid_search_ids = [
        "../etc/passwd",
        "../../runs",
        "search/123",
        "search\\123",
        "search 123",
        "search_123\n",
        "search_123; rm -rf /",
    ]

    for search_id in invalid_search_ids:
        with pytest.raises(ValidationError):
            SetupSearchRequest(
                search_id=search_id,
                brief_notes="Notes",
                jd_content="JD text",
            )
