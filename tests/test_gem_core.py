import pytest
import httpx
from unittest.mock import AsyncMock
from utils.gem_core import GEMClient


@pytest.mark.asyncio
async def test_gem_client_reuses_persistent_client():
    client = GEMClient(db_url="http://test-db:8000")
    c1 = client._get_client()
    c2 = client._get_client()
    assert c1 is c2
    assert not c1.is_closed
    await client.close()
    assert c1.is_closed


@pytest.mark.asyncio
async def test_gem_client_context_manager():
    async with GEMClient(db_url="http://test-db:8000") as gem_client:
        active_client = gem_client._get_client()
        assert not active_client.is_closed
    assert active_client.is_closed


@pytest.mark.asyncio
async def test_gem_client_methods_success():
    mock_http_client = httpx.AsyncClient()
    req = httpx.Request("POST", "http://test-db:8000/entity/upsert")
    mock_resp = httpx.Response(200, json={"status": "ok"}, request=req)
    mock_http_client.post = AsyncMock(return_value=mock_resp)

    gem_client = GEMClient(
        db_url="http://test-db:8000", client=mock_http_client
    )

    upsert_res = await gem_client.upsert_entity({"id": "1"})
    assert upsert_res == {"status": "ok"}
    mock_http_client.post.assert_called_with(
        "http://test-db:8000/entity/upsert", json={"id": "1"}
    )

    discard_res = await gem_client.discard_entity({"id": "2"})
    assert discard_res == {"status": "ok"}
    mock_http_client.post.assert_called_with(
        "http://test-db:8000/entity/discard", json={"id": "2"}
    )

    log_res = await gem_client.log_execution({"log": "data"})
    assert log_res == {"status": "ok"}
    mock_http_client.post.assert_called_with(
        "http://test-db:8000/log/discovery", json={"log": "data"}
    )

    assert mock_http_client.post.call_count == 3
    await gem_client.close()


@pytest.mark.asyncio
async def test_gem_client_handles_error():
    mock_http_client = httpx.AsyncClient()
    mock_http_client.post = AsyncMock(
        side_effect=Exception("Connection refused")
    )

    gem_client = GEMClient(
        db_url="http://test-db:8000", client=mock_http_client
    )

    res = await gem_client.upsert_entity({"id": "fail"})
    assert res is None

    res = await gem_client.discard_entity({"id": "fail"})
    assert res is None

    res = await gem_client.log_execution({"id": "fail"})
    assert res is None

    await gem_client.close()
