import asyncio
import time
import os
import sys
from unittest.mock import MagicMock

sys.path.append(os.getcwd())
from utils.gem_core import GEMClient

# Mock server to respond to requests
from fastapi import FastAPI
import uvicorn
import threading

app = FastAPI()
@app.post("/entity/upsert")
async def upsert():
    return {"status": "success"}

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

async def benchmark():
    client = GEMClient(db_url="http://127.0.0.1:8001")
    data = {"entity_id": "test", "current_stage": "test", "state": "test", "agent_responsible": "test", "trace_id": "test"}

    # Pre-warm
    try:
        await client.upsert_entity(data)
    except:
        pass

    start = time.perf_counter()
    n = 20
    for _ in range(n):
        await client.upsert_entity(data)
    end = time.perf_counter()

    print(f"Average upsert_entity time (with new client every time): {(end - start) / n * 1000:.4f} ms")

if __name__ == "__main__":
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(2) # Wait for server to start
    asyncio.run(benchmark())
