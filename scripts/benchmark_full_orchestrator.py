import asyncio
import time
import os
import sys
from unittest.mock import MagicMock, AsyncMock

sys.path.append(os.getcwd())
from agent.gem6.orchestrator import GEM6Orchestrator

async def benchmark_orchestrator():
    # Mock dependencies
    gemini_mock = MagicMock()
    gemini_mock.run_gem.return_value = {
        "json": {"action": "finalize", "status": "SUCCESS", "final_output": {"result": "ok"}},
        "markdown": "Done",
        "raw": '{"action": "finalize", "status": "SUCCESS", "final_output": {"result": "ok"}}',
        "usage": {"total_tokens": 100}
    }

    # Mock DB Client to avoid HTTP calls
    orch = GEM6Orchestrator(gemini=gemini_mock)
    orch.client = AsyncMock()
    orch.client.upsert_entity.return_value = {"status": "success"}
    orch.client.log_execution.return_value = {"status": "logged"}

    search_inputs = {"job": "Engineer"}
    candidates = {"cand1": {"name": "Alice"}}

    start = time.perf_counter()
    for _ in range(10):
        await orch.run_pipeline(search_inputs, candidates)
    end = time.perf_counter()

    avg_time = (end - start) / 10 * 1000
    print(f"Average run_pipeline (1 candidate, 1 step) time: {avg_time:.4f} ms")

if __name__ == "__main__":
    asyncio.run(benchmark_orchestrator())
