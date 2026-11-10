import pytest
import httpx
from utils.gem_core import GEMClient


@pytest.mark.asyncio
async def test_gem_client_connection_reuse():
    """Verify that GEMClient reuses the persistent httpx.AsyncClient instance across calls."""
    client = GEMClient("http://test-server:8000")
    assert client._client is None

    # First call instantiates client
    c1 = client._get_client()
    assert isinstance(c1, httpx.AsyncClient)
    assert not c1.is_closed

    # Successive calls reuse identical client
    c2 = client._get_client()
    assert c1 is c2

    # Cleanup
    await client.close()
    assert client._client is None
    assert c1.is_closed


@pytest.mark.asyncio
async def test_gem_client_context_manager():
    """Verify that GEMClient can be used as an async context manager."""
    async with GEMClient("http://test-server:8000") as client:
        c = client._get_client()
        assert not c.is_closed

    assert client._client is None
    assert c.is_closed


@pytest.mark.asyncio
async def test_gem_client_reopens_after_close():
    """Verify that GEMClient safely creates a new client session if used after close()."""
    client = GEMClient("http://test-server:8000")
    c1 = client._get_client()
    await client.close()
    assert c1.is_closed

    c2 = client._get_client()
    assert c2 is not c1
    assert not c2.is_closed
    await client.close()
    assert c2.is_closed
