import pytest
import httpx
from utils.gem_core import GEMClient

@pytest.mark.asyncio
async def test_gem_client_connection_reuse():
    client = GEMClient("http://localhost:8000")
    assert client._client is None

    # First call initializes client
    c1 = client._get_client()
    assert isinstance(c1, httpx.AsyncClient)
    assert not c1.is_closed

    # Second call reuses same client instance
    c2 = client._get_client()
    assert c1 is c2

    # Clean up
    await client.close()
    assert c1.is_closed

@pytest.mark.asyncio
async def test_gem_client_context_manager():
    async with GEMClient("http://localhost:8000") as client:
        c1 = client._get_client()
        assert not c1.is_closed

    assert c1.is_closed

@pytest.mark.asyncio
async def test_gem_client_external_client():
    external = httpx.AsyncClient()
    client = GEMClient("http://localhost:8000", client=external)
    assert client._get_client() is external

    await client.close()
    # Does not close external client because _owner is False
    assert not external.is_closed
    await external.aclose()
