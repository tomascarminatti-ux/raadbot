import asyncio
import time
import os
import sys
from unittest.mock import MagicMock, AsyncMock

# Add project root to sys.path
sys.path.append(os.getcwd())

from agent.gem6.orchestrator import GEM6Orchestrator

async def benchmark():
    print("🚀 Starting Pipeline Benchmark...")

    # Mock GeminiClient
    mock_gemini = MagicMock()
    # Mock run_gem to simulate LLM latency (e.g., 0.5s)
    def mocked_run_gem(prompt, gem_name=None):
        time.sleep(0.5) # Simulate LLM processing time
        return {
            "json": {
                "action": "finalize",
                "thought": "Mocked thought",
                "status": "SUCCESS",
                "final_output": {"score": 1.0}
            }
        }
    mock_gemini.run_gem.side_effect = mocked_run_gem

    search_inputs = {"job": "Engineer"}
    # 5 candidates
    num_candidates = 5
    candidates = {f"CAND-{i:03d}": {"name": f"Candidate {i}"} for i in range(num_candidates)}

    orchestrator = GEM6Orchestrator(gemini=mock_gemini)
    # Patch the db client to avoid real network calls
    orchestrator.client.upsert_entity = AsyncMock(return_value={})
    orchestrator.client.log_execution = AsyncMock(return_value={})

    start_time = time.perf_counter()
    results = await orchestrator.run_pipeline(search_inputs, candidates)
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"\n⏱️  Total Pipeline Duration: {duration:.4f} seconds")
    print(f"📊 Average per Candidate: {duration/num_candidates:.4f} seconds")
    print(f"✅ Processed {len(results)} candidates")

    # Expected sequential time: 5 * 0.5 = 2.5 seconds + overhead
    # Expected parallel time: 0.5 seconds + overhead (if run_gem is not blocking)

    return duration

if __name__ == "__main__":
    asyncio.run(benchmark())
