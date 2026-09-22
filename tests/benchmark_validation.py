"""
benchmark_validation.py - Measures performance difference between uncompiled
jsonschema.validate and compiled validator reuse.
"""

import time
import jsonschema
from jsonschema.validators import validator_for
from agent.pipeline import Pipeline


def benchmark_schema_validation(iterations: int = 2000):
    pipeline = Pipeline(None, "BENCHMARK-001", "/tmp/benchmark_output")
    sample_json = {
        "meta": {
            "search_id": "SEARCH-2024-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2025-01-01T00:00:00Z",
            "sources": ["cv"],
        },
        "scores": {"score_dimension": 8, "confidence": 9},
        "blockers": [],
        "content": {"summary": "benchmark test content"},
    }

    # 1. Uncompiled jsonschema.validate
    start = time.perf_counter()
    for _ in range(iterations):
        jsonschema.validate(instance=sample_json, schema=pipeline.schema)
    uncompiled_time = time.perf_counter() - start

    # 2. Pre-compiled validator reuse (used by pipeline._validate_output)
    start = time.perf_counter()
    for _ in range(iterations):
        pipeline._validate_output(sample_json, "gem1")
    compiled_time = time.perf_counter() - start

    speedup = uncompiled_time / compiled_time if compiled_time > 0 else float("inf")

    print(f"Iterations: {iterations}")
    print(f"Uncompiled jsonschema.validate: {uncompiled_time:.4f}s")
    print(f"Pre-compiled Pipeline validator: {compiled_time:.4f}s")
    print(f"Speedup: {speedup:.2f}x")

    return uncompiled_time, compiled_time, speedup


if __name__ == "__main__":
    benchmark_schema_validation()
