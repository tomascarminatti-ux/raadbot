import asyncio
import time
import os
import sys
from unittest.mock import MagicMock, patch

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.getcwd())

from agent.gem6.orchestrator import GEM6Orchestrator

async def benchmark_orchestrator():
    print("🚀 Benchmarking Orchestrator...")

    # Mocking Gemini to simulate delay
    mock_gemini = MagicMock()

    def mock_run_gem(*args, **kwargs):
        time.sleep(0.1) # Simulate network/processing latency
        gem_name = kwargs.get("gem_name", "")
        if gem_name == "gem6":
            return {"json": {"action": "finalize", "status": "SUCCESS", "thought": "Done"}}
        return {"json": {"score": 0.9}}

    mock_gemini.run_gem.side_effect = mock_run_gem

    orchestrator = GEM6Orchestrator(mock_gemini, "runs/benchmark", config={"search_id": "BENCH"})

    search_inputs = {"job": "Engineer"}
    candidates = {f"CAND-{i}": {"data": i} for i in range(10)}

    start_time = time.perf_counter()
    await orchestrator.run_pipeline(search_inputs, candidates)
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"Total duration for 10 candidates: {duration:.4f}s")
    print(f"Average time per candidate: {duration/10:.4f}s")

if __name__ == "__main__":
    asyncio.run(benchmark_orchestrator())
