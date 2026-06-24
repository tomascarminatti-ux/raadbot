import asyncio
import time
import os
import sys
from unittest.mock import AsyncMock

# Ensure project root is in path
sys.path.append(os.getcwd())

from agent.gem6.orchestrator import GEM6Orchestrator  # noqa: E402


class MockGemini:
    def run_gem(self, prompt, gem_name=None):
        # Simulate network latency
        time.sleep(0.1)
        # Return a decision to finalize immediately for speed of benchmark
        return {
            "json": {
                "action": "finalize",
                "thought": "Mocked thought",
                "status": "SUCCESS",
                "final_output": {"score": 0.9}
            }
        }


async def benchmark():
    print("--- Starting Benchmark (Optimized) ---")
    gemini = MockGemini()

    orch = GEM6Orchestrator(gemini=gemini, output_dir="runs/benchmark", search_id="BENCH-001")
    orch.client = AsyncMock()  # Mock the DB client to avoid network calls

    search_inputs = {"job": "Engineer"}
    candidates = {f"CAND-{i}": {"name": f"Candidate {i}"} for i in range(5)}

    start_time = time.time()
    results = await orch.run_pipeline(search_inputs, candidates)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Processed {len(candidates)} candidates in {total_time:.4f} seconds")

    # Verify results
    assert len(results) == 5
    for cid in candidates:
        assert cid in results
        assert results[cid]["status"] == "SUCCESS"

    print("Benchmark completed successfully and verified results.")
    return total_time


if __name__ == "__main__":
    asyncio.run(benchmark())
