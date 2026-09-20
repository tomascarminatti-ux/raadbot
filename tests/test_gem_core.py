import pytest
import httpx
from utils.gem_core import GEMClient

@pytest.mark.asyncio
async def test_gem_client_connection_reuse():
    client = GEMClient(db_url="http://mock-db:8000")

    # Client should initially be None
    assert client._client is None

    # Internal _get_client should initialize httpx.AsyncClient
    httpx_client = client._get_client()
    assert isinstance(httpx_client, httpx.AsyncClient)
    assert not httpx_client.is_closed
    assert client._owns_client is True

    # Second call should return the exact same instance
    second_httpx_client = client._get_client()
    assert second_httpx_client is httpx_client

    # Close should clean up the instance
    await client.close()
    assert client._client is None
    assert httpx_client.is_closed

@pytest.mark.asyncio
async def test_gem_client_context_manager():
    async with GEMClient(db_url="http://mock-db:8000") as client:
        httpx_client = client._get_client()
        assert not httpx_client.is_closed

    # Should be closed after exiting context block
    assert client._client is None
    assert httpx_client.is_closed

@pytest.mark.asyncio
async def test_gem_client_provided_client():
    external_client = httpx.AsyncClient()
    client = GEMClient(db_url="http://mock-db:8000", client=external_client)

    httpx_client = client._get_client()
    assert httpx_client is external_client
    assert client._owns_client is False

    await client.close()
    # External client should NOT be closed by GEMClient
    assert not external_client.is_closed
    await external_client.aclose()
