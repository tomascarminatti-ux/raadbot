"""
benchmark_validation.py – Benchmarks jsonschema.validate vs pre-compiled validator in Pipeline.
"""

import time
from agent.pipeline import Pipeline
from jsonschema import validate


def run_benchmark(iterations: int = 2000):
    pipeline = Pipeline(None, "SEARCH-2025-001", "runs/benchmark_tmp")

    valid_json = {
        "meta": {
            "search_id": "SEARCH-2025-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2025-01-01T00:00:00Z",
            "sources": ["cv"],
        },
        "scores": {"confidence": 8, "score_dimension": 8},
        "blockers": [],
        "content": {},
    }

    # Standard jsonschema.validate
    start_time = time.perf_counter()
    for _ in range(iterations):
        validate(instance=valid_json, schema=pipeline.schema)
    std_elapsed = time.perf_counter() - start_time

    # Pre-compiled validator in Pipeline
    start_time = time.perf_counter()
    for _ in range(iterations):
        pipeline._validate_output(valid_json, "gem1")
    compiled_elapsed = time.perf_counter() - start_time

    speedup = std_elapsed / compiled_elapsed if compiled_elapsed > 0 else 0.0

    print(f"Iterations: {iterations}")
    print(f"Standard jsonschema.validate: {std_elapsed:.4f}s")
    print(f"Pipeline compiled validator: {compiled_elapsed:.4f}s")
    print(f"Speedup: {speedup:.2f}x faster")


if __name__ == "__main__":
    run_benchmark()
