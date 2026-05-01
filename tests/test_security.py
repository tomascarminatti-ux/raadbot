
import pytest
from httpx import AsyncClient, ASGITransport
from api import app
from infra.db.api import app as db_app

@pytest.mark.asyncio
async def test_api_path_traversal_search_id():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/run", json={
            "search_id": "../../etc/passwd",
            "local_dir": "test",
            "model": "gemini-2.0-flash"
        })
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_api_path_traversal_local_dir():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/run", json={
            "search_id": "valid_id",
            "local_dir": "../outside",
            "model": "gemini-2.0-flash"
        })
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_api_path_traversal_gem_id():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/gems/refine", json={
            "gem_id": "../api",
            "instruction": "test"
        })
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_db_path_traversal_entity_id():
    transport = ASGITransport(app=db_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/entity/upsert", json={
            "entity_id": "../../malicious",
            "current_stage": "gem1",
            "state": "active",
            "agent_responsible": "gem1",
            "trace_id": "valid_trace"
        })
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_db_path_traversal_trace_id():
    transport = ASGITransport(app=db_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/entity/discard", json={
            "entity_id": "valid_id",
            "stage_at_discard": "gem1",
            "reason": "test",
            "agent_responsible": "gem1",
            "trace_id": "invalid/path"
        })
        assert response.status_code == 422
