import httpx
import time
import asyncio

async def measure_overhead():
    start = time.perf_counter()
    for _ in range(100):
        async with httpx.AsyncClient() as client:
            pass
    end = time.perf_counter()
    print(f"100 AsyncClient creations: {end - start:.4f}s")

if __name__ == "__main__":
    asyncio.run(measure_overhead())
