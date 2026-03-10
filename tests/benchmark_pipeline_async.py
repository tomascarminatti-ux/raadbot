
import asyncio
import time
import os
import sys
from unittest.mock import MagicMock, AsyncMock

# Add current directory to path
sys.path.append(os.getcwd())

from agent.gemini_client import GeminiClient
from agent.gem6.orchestrator import GEM6Orchestrator

async def benchmark_parallel():
    # Mock GeminiClient
    mock_gemini = MagicMock(spec=GeminiClient)

    # We'll use an async side effect that sleeps and returns a dummy result
    async def async_side_effect(*args, **kwargs):
        await asyncio.sleep(0.1)
        return {"json": {"action": "finalize", "status": "SUCCESS", "final_output": {}}, "markdown": "", "usage": {}}

    mock_gemini.run_gem = AsyncMock(side_effect=async_side_effect)

    orchestrator = GEM6Orchestrator(gemini=mock_gemini, search_id="BENCH-PAR")

    search_inputs = {"brief": "test"}
    candidates = {f"CAND-{i}": {"data": i} for i in range(10)}

    print(f"Starting parallel benchmark with {len(candidates)} candidates...")
    start_time = time.perf_counter()
    await orchestrator.run_pipeline(search_inputs, candidates)
    end_time = time.perf_counter()

    print(f"Parallel time: {end_time - start_time:.4f}s")
    return end_time - start_time

if __name__ == "__main__":
    asyncio.run(benchmark_parallel())
