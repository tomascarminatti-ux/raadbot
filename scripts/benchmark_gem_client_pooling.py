import time
import asyncio
import os
import sys
import httpx

# Add root to path
sys.path.append(os.getcwd())

from utils.gem_core import GEMClient

async def benchmark_gem_client():
    client = GEMClient("http://localhost:8000")
    # First call to initialize
    await client.log_execution({"test": "data"})

    start = time.perf_counter()
    n = 10
    for _ in range(n):
        await client.log_execution({"test": "data"})
    end = time.perf_counter()
    print(f"GEMClient call time: {(end - start) / n:.4f}s")
    await client.aclose()

if __name__ == "__main__":
    asyncio.run(benchmark_gem_client())
