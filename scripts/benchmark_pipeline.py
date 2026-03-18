import asyncio
import time
import os
import shutil
import json
from unittest.mock import AsyncMock, MagicMock
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

async def benchmark():
    output_dir = "benchmark_outputs"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    mock_gemini = MagicMock(spec=GeminiClient)
    mock_gemini.run_gem_async = AsyncMock()

    # Mock return value for any GEM
    mock_gemini.run_gem_async.return_value = {
        "json": {
            "meta": {
                "search_id": "BENCHMARK",
                "gem": "GEM",
                "prompt_version": "v1.2",
                "timestamp": "2024-01-01T00:00:00Z",
                "sources": ["test"]
            },
            "scores": {"confidence": 8, "score_dimension": 8},
            "blockers": [],
            "content": {"problema_real_del_rol": "test challenge"},
            "decision": "APROBADO"
        },
        "markdown": "# Mock Output",
        "usage": {"prompt_tokens": 100, "candidates_tokens": 50}
    }

    search_inputs = {
        "jd_text": "test jd",
        "kickoff_notes": "test kickoff",
        "company_context": "test company",
        "client_culture": "test culture"
    }

    # 50 candidates to make the I/O and redundant work more visible
    candidates = {f"CAND-{i:03d}": {
        "cv_text": "test cv",
        "interview_notes": "test interview",
        "tests_text": "test tests",
        "case_notes": "test case",
        "references_text": "test refs"
    } for i in range(50)}

    pipeline = Pipeline(mock_gemini, "BENCHMARK", output_dir)

    # Warm up (if any)
    # await pipeline.run_full_pipeline(search_inputs, {"CAND-WARM": candidates["CAND-000"]})

    start_time = time.perf_counter()
    await pipeline.run_full_pipeline(search_inputs, candidates)
    end_time = time.perf_counter()

    print(f"\n[BENCHMARK] Time taken for 50 candidates: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    asyncio.run(benchmark())
