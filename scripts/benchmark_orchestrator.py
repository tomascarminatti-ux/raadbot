import asyncio
import time
import os
import sys
from unittest.mock import MagicMock, AsyncMock

# Add project root to path
sys.path.append(os.getcwd())

from agent.gem6.orchestrator import GEM6Orchestrator

async def mock_run_gem(prompt, gem_name=None):
    # Simulate LLM latency
    await asyncio.sleep(0.1)
    if gem_name == "gem6":
        return {
            "json": {
                "thought": "Thinking...",
                "action": "call_agent",
                "agent_id": "gem1",
                "payload": {}
            }
        }
    return {"json": {"score": 0.8}, "markdown": "Result"}

async def mock_run_gem_finalize(prompt, gem_name=None):
    await asyncio.sleep(0.1)
    if gem_name == "gem6":
        return {
            "json": {
                "thought": "Finalizing",
                "action": "finalize",
                "status": "SUCCESS",
                "final_output": {"result": "ok"}
            }
        }
    return {"json": {"score": 0.8}}

class MockGemini:
    def __init__(self):
        self.call_count = 0

    def run_gem(self, prompt, gem_name=None):
        self.call_count += 1
        # First 2 calls for each candidate are reasoning, then 3rd is finalize
        # But wait, the loop in orchestrator is complex.
        # Let's just use a simple stateful mock or just return finalize after some steps.
        # Actually, for benchmarking parallelism, we just need them to take time.

        # We can't easily use await inside run_gem because it's synchronous in GeminiClient
        # Wait, GeminiClient.run_gem IS synchronous.
        time.sleep(0.1) # Simulate synchronous LLM call

        if gem_name == "gem6":
            # Toggle between call_agent and finalize to simulate a short loop
            if self.call_count % 3 == 0:
                return {
                    "json": {
                        "thought": "Finalizing",
                        "action": "finalize",
                        "status": "SUCCESS",
                        "final_output": {"result": "ok"}
                    }
                }
            return {
                "json": {
                    "thought": "Thinking...",
                    "action": "call_agent",
                    "agent_id": "gem1",
                    "payload": {}
                }
            }
        return {"json": {"score": 0.8}}

async def run_benchmark(num_candidates=10):
    gemini = MockGemini()
    orchestrator = GEM6Orchestrator(gemini=gemini, search_id="BENCHMARK", output_dir="runs/benchmark")

    # Mock GEMClient to avoid DB calls
    orchestrator.client = MagicMock()
    orchestrator.client.upsert_entity = AsyncMock()
    orchestrator.client.log_execution = AsyncMock()

    search_inputs = {"test": "data"}
    candidates = {f"CAND-{i}": {"data": "test"} for i in range(num_candidates)}

    print(f"🚀 Starting benchmark with {num_candidates} candidates...")
    start_time = time.perf_counter()

    await orchestrator.run_pipeline(search_inputs, candidates)

    end_time = time.perf_counter()
    total_time = end_time - start_time

    print(f"⏱️ Total time: {total_time:.4f}s")
    print(f"⏱️ Average time per candidate: {total_time/num_candidates:.4f}s")
    return total_time

if __name__ == "__main__":
    asyncio.run(run_benchmark())
