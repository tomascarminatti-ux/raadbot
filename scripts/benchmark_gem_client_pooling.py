import asyncio
import time
import os
import sys
import httpx
from typing import Dict, Any

sys.path.append(os.getcwd())

class PersistentGEMClient:
    def __init__(self, db_url: str = "http://db-api:8000"):
        self.db_url = db_url
        self.client = httpx.AsyncClient()

    async def upsert_entity(self, data: Dict[str, Any]):
        resp = await self.client.post(f"{self.db_url}/entity/upsert", json=data)
        return resp.json()

    async def close(self):
        await self.client.aclose()

from scripts.benchmark_gem_client_overhead import app
import uvicorn
import threading

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8002, log_level="error")

async def benchmark():
    client = PersistentGEMClient(db_url="http://127.0.0.1:8002")
    data = {"entity_id": "test", "current_stage": "test", "state": "test", "agent_responsible": "test", "trace_id": "test"}

    # Pre-warm
    await client.upsert_entity(data)

    start = time.perf_counter()
    n = 20
    for _ in range(n):
        await client.upsert_entity(data)
    end = time.perf_counter()

    print(f"Average upsert_entity time (with persistent client): {(end - start) / n * 1000:.4f} ms")
    await client.close()

if __name__ == "__main__":
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(2)
    asyncio.run(benchmark())
