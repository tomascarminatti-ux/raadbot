
import asyncio
import time
import os
import shutil
import sys
from unittest.mock import AsyncMock, MagicMock

# Ensure we can import from the agent directory
sys.path.append(os.getcwd())

from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

async def mock_gem_call(prompt, *args, **kwargs):
    # Simulate some processing time but no actual network I/O
    # time.sleep(0.01) # This would block the loop!
    await asyncio.sleep(0.05)

    # Try to guess which gem is being called to pass validation
    import re
    gem_match = re.search(r"GEM_NAME:\s*(gem\d+)", prompt)
    gem_name = gem_match.group(1).upper() if gem_match else "GEM_1"
    if gem_name == "GEM1": gem_name = "GEM_1"
    if gem_name == "GEM2": gem_name = "GEM_2"
    if gem_name == "GEM3": gem_name = "GEM_3"
    if gem_name == "GEM4": gem_name = "GEM_4"
    if gem_name == "GEM5": gem_name = "GEM_5"

    return {
        "json": {
            "meta": {"search_id": "SEARCH-2024-001", "gem": gem_name, "prompt_version": "v1.0", "timestamp": "2024-01-01T00:00:00Z", "sources": ["test.txt"]},
            "scores": {"score_dimension": 8, "confidence": 8},
            "blockers": [],
            "content": {"problema_real_del_rol": "test"}
        },
        "markdown": "some content",
        "raw": "raw content",
        "usage": {"prompt_tokens": 100, "candidates_tokens": 50}
    }

async def run_benchmark():
    output_dir = "bench_outputs"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    mock_gemini = MagicMock(spec=GeminiClient)
    mock_gemini.run_gem_async = AsyncMock(side_effect=mock_gem_call)

    # Note: Pipeline constructor calls _load_state and _load_schema synchronously
    pipeline = Pipeline(mock_gemini, "SEARCH-2024-001", output_dir)

    search_inputs = {"jd_text": "test"}
    # 20 candidates to see some concurrency
    candidates = {f"CAND-{i:03d}": {"cv_text": "test"} for i in range(20)}

    print(f"Starting pipeline for {len(candidates)} candidates...")
    start_time = time.perf_counter()
    await pipeline.run_full_pipeline(search_inputs, candidates)
    end_time = time.perf_counter()

    print(f"\nTotal time for {len(candidates)} candidates: {end_time - start_time:.4f} seconds")

    # Cleanup
    # if os.path.exists(output_dir):
    #     shutil.rmtree(output_dir)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
