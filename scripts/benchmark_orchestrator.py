
import time
import os
import sys
import asyncio
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime, timezone

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

async def benchmark_orchestration():
    gemini_mock = MagicMock(spec=GeminiClient)
    # Mock run_gem_async to return a dummy result that passes validation
    async def dummy_run_gem(prompt):
        # Determine which gem is being called from the prompt (hacky but works for mock)
        gem_id = "GEM_1"
        if "gem2" in prompt.lower(): gem_id = "GEM_2"
        elif "gem3" in prompt.lower(): gem_id = "GEM_3"
        elif "gem4" in prompt.lower(): gem_id = "GEM_4"
        elif "gem5" in prompt.lower(): gem_id = "GEM_5"

        await asyncio.sleep(0.01) # 10ms simulated latency

        res = {
            "meta": {
                "search_id": "SEARCH-2026-001",
                "candidate_id": "CAND-001",
                "gem": gem_id,
                "prompt_version": "v1.0",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "sources": ["test"]
            },
            "scores": {
                "score_dimension": 8,
                "confidence": 9
            },
            "blockers": [],
            "content": {"problema_real_del_rol": "Test challenge"},
        }
        if gem_id == "GEM_4":
            res["decision"] = "APROBADO"

        return {
            "json": res,
            "markdown": "Result",
            "raw": "Result",
            "usage": {"prompt_tokens": 100, "candidates_tokens": 50}
        }

    gemini_mock.run_gem_async = AsyncMock(side_effect=dummy_run_gem)

    search_id = "SEARCH-2026-001"
    output_dir = "runs/bench-output"
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    pipeline = Pipeline(gemini_mock, search_id, output_dir)

    search_inputs = {"jd_text": "JD", "kickoff_notes": "Notes"}
    candidates = {f"CAND-{i}": {"cv_text": "CV"} for i in range(10)}

    start_time = time.time()
    await pipeline.run_full_pipeline(search_inputs, candidates)
    end_time = time.time()

    print(f"\nTotal time for 10 candidates in parallel: {end_time - start_time:.4f} s")

if __name__ == "__main__":
    asyncio.run(benchmark_orchestration())
