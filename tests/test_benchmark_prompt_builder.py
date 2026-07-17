import time
import pytest
from agent.prompt_builder import build_prompt, load_prompt

def test_benchmark_prompt_builder():
    variables = {
        "kickoff_notes": "Senior Data Engineer needed with Python and SQL experience.",
        "brief_jd": "We are looking for a Senior Data Engineer to join our growing team.",
        "company_context": "Fast-growing fintech startup in Madrid.",
        "input": {
            "search_id": "SEARCH-2026-001",
            "roles": ["Data Engineer", "ML Engineer"],
            "requirements": {
                "experience": 5,
                "skills": ["Python", "AWS", "Spark"]
            }
        }
    }

    # Warm-up
    for _ in range(10):
        _ = build_prompt("gem5", {"input": variables})

    # Benchmark
    start_time = time.perf_counter()
    iterations = 500
    for _ in range(iterations):
        _ = build_prompt("gem5", {"input": variables})
    end_time = time.perf_counter()

    duration = end_time - start_time
    avg_time_ms = (duration / iterations) * 1000
    print(f"\n[BENCHMARK] Average build_prompt execution time: {avg_time_ms:.4f} ms per call")
    assert avg_time_ms > 0
