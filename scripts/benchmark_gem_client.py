import asyncio
import time
import os
import sys
from unittest.mock import MagicMock, AsyncMock

sys.path.append(os.getcwd())
from utils.gem_core import GEMClient

async def benchmark():
    # We need a server to actually test connection pooling benefit,
    # but we can also just measure the overhead of creating the client.
    client = GEMClient(db_url="http://localhost:8001") # Dummy URL

    start = time.perf_counter()
    n = 100
    for _ in range(n):
        # This will fail/timeout, but we want to see the time taken before the actual request if possible,
        # or just mock the request but keep the client creation.
        pass

    # Real test: how much time does it take to just do 'async with httpx.AsyncClient()'?
    import httpx
    start = time.perf_counter()
    for _ in range(n):
        async with httpx.AsyncClient() as c:
            pass
    end = time.perf_counter()
    avg_time = (end - start) / n * 1000
    print(f"Average 'async with httpx.AsyncClient()' overhead: {avg_time:.4f} ms")

if __name__ == "__main__":
    asyncio.run(benchmark())
