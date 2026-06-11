import asyncio
import time
import os
import sys
from unittest.mock import MagicMock, AsyncMock

# Ensure project root is in path
sys.path.append(os.getcwd())

from agent.gem6.orchestrator import GEM6Orchestrator

class MockGeminiClient:
    def __init__(self, delay=0.1):
        self.delay = delay

    def run_gem(self, prompt, gem_name=None):
        # Simulate LLM processing time
        time.sleep(self.delay)

        # Return a decision to finalize after 1 step to keep benchmark fast but representative
        if gem_name == "gem6":
            return {
                "json": {
                    "action": "finalize",
                    "thought": "Mocking completion",
                    "status": "SUCCESS",
                    "final_output": {"score": 0.95}
                }
            }
        return {"json": {}}

async def run_benchmark():
    print("--- Pipeline Benchmark ---")

    # 5 candidates to process
    candidates = {f"CAND-{i:03d}": {"data": "mock"} for i in range(5)}
    search_inputs = {"query": "test"}

    # Setup orchestrator with mock client
    mock_gemini = MockGeminiClient(delay=0.5) # 0.5s per LLM call
    orchestrator = GEM6Orchestrator(gemini=mock_gemini, output_dir="runs/benchmark")

    # Mock GEMClient to avoid DB calls
    orchestrator.client = AsyncMock()

    start_time = time.perf_counter()

    print(f"Processing {len(candidates)} candidates...")
    await orchestrator.run_pipeline(search_inputs, candidates)

    end_time = time.perf_counter()
    total_time = end_time - start_time

    print(f"Total time: {total_time:.4f} seconds")
    print(f"Average time per candidate: {total_time/len(candidates):.4f} seconds")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
