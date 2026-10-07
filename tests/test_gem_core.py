import pytest
import httpx
from utils.gem_core import GEMClient


@pytest.mark.asyncio
async def test_gem_client_session_reuse():
    client = GEMClient("http://localhost:8000")
    assert client._client is None

    # First call initializes the httpx client
    c1 = client._get_client()
    assert isinstance(c1, httpx.AsyncClient)
    assert not c1.is_closed

    # Second call returns the exact same client instance
    c2 = client._get_client()
    assert c2 is c1

    await client.close()
    assert client._client is None
    assert c1.is_closed


@pytest.mark.asyncio
async def test_gem_client_context_manager():
    async with GEMClient("http://localhost:8000") as client:
        c1 = client._get_client()
        assert not c1.is_closed

    # After exiting context manager, client session should be closed
    assert client._client is None
    assert c1.is_closed
