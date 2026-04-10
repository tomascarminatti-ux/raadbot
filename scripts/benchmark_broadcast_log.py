import asyncio
import time
import os
import sys
import json

sys.path.append(os.getcwd())
from utils.ws_logger import broadcast_log

async def benchmark():
    data = {
        "gem": "GEM1",
        "action": "Procesamiento completado",
        "score": 0.8,
        "status": "OK",
        "output_preview": "test output...",
        "entity_id": "CAND1",
        "step": 1
    }

    # Pre-warm
    await broadcast_log(data)

    start = time.perf_counter()
    n = 100
    for _ in range(n):
        await broadcast_log(data)
    end = time.perf_counter()

    avg_time = (end - start) / n * 1000
    print(f"Average broadcast_log time: {avg_time:.4f} ms")

if __name__ == "__main__":
    asyncio.run(benchmark())
