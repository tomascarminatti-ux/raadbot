import asyncio
import time
import os
import sys
import httpx

async def benchmark():
    n = 100

    # 1. New client every time
    start = time.perf_counter()
    for _ in range(n):
        async with httpx.AsyncClient() as c:
            pass
    end = time.perf_counter()
    print(f"New client every time: {(end - start) / n * 1000:.4f} ms")

    # 2. Reuse client
    start = time.perf_counter()
    async with httpx.AsyncClient() as c:
        for _ in range(n):
            pass
    end = time.perf_counter()
    print(f"Reused client: {(end - start) / n * 1000:.4f} ms")

if __name__ == "__main__":
    asyncio.run(benchmark())
