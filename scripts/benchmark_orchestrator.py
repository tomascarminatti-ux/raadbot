import asyncio
import time
import os
import sys
import json
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.getcwd())

from agent.gem6.orchestrator import GEM6Orchestrator

async def mock_run_gem(*args, **kwargs):
    # Simulate LLM delay
    await asyncio.sleep(0.5)
    # Return a "finalize" action to keep it short
    return {
        "json": {
            "thought": "Mock thought",
            "action": "finalize",
            "status": "SUCCESS",
            "final_output": {"score": 0.9}
        }
    }

def sync_mock_run_gem(*args, **kwargs):
    # Simulate LLM delay
    time.sleep(0.5)
    return {
        "json": {
            "thought": "Mock thought",
            "action": "finalize",
            "status": "SUCCESS",
            "final_output": {"score": 0.9}
        }
    }

async def run_benchmark():
    print("🚀 Starting benchmark...")

    # Setup mock gemini client
    mock_gemini = MagicMock()
    mock_gemini.run_gem.side_effect = sync_mock_run_gem

    orchestrator = GEM6Orchestrator(gemini=mock_gemini)

    search_inputs = {"role": "Engineer"}
    candidates = {f"CAND-{i}": {"name": f"Candidate {i}"} for i in range(10)}

    start_time = time.perf_counter()

    # We need to mock the DB client calls as well to avoid actual HTTP requests
    with patch.object(orchestrator.client, 'upsert_entity', return_value=asyncio.Future()):
        orchestrator.client.upsert_entity.set_result({})
        with patch.object(orchestrator.client, 'log_execution', return_value=asyncio.Future()):
            orchestrator.client.log_execution.set_result({})
            with patch('agent.gem6.orchestrator.broadcast_log', return_value=asyncio.Future()):
                # Fix for broadcast_log return_value
                from agent.gem6.orchestrator import broadcast_log
                import agent.gem6.orchestrator
                agent.gem6.orchestrator.broadcast_log = MagicMock(side_effect=lambda x: asyncio.sleep(0))

                await orchestrator.run_pipeline(search_inputs, candidates)

    end_time = time.perf_counter()
    duration = end_time - start_time

    print(f"⏱️ Total duration for 10 candidates: {duration:.2f} seconds")
    print(f"Average time per candidate: {duration/10:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
