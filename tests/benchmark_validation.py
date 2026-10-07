"""
benchmark_validation.py – Benchmarks uncompiled jsonschema.validate vs compiled validator.validate.
"""

import json
import os
import time
from jsonschema import validate
from jsonschema.validators import validator_for


def run_benchmark():
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    validator = validator_for(schema)(schema)

    dummy_data = {
        "meta": {
            "search_id": "SEARCH-2024-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["cv.txt"],
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9,
        },
        "blockers": [],
        "content": {"summary": "test"},
    }

    # Warmup
    validate(instance=dummy_data, schema=schema)
    validator.validate(dummy_data)

    iterations = 2000

    # Uncompiled validation
    start = time.perf_counter()
    for _ in range(iterations):
        validate(instance=dummy_data, schema=schema)
    duration_uncompiled = time.perf_counter() - start

    # Compiled validation
    start = time.perf_counter()
    for _ in range(iterations):
        validator.validate(dummy_data)
    duration_compiled = time.perf_counter() - start

    speedup = duration_uncompiled / duration_compiled

    print(f"Benchmark over {iterations} iterations:")
    print(f"  Uncompiled jsonschema.validate: {duration_uncompiled:.4f}s")
    print(f"  Compiled validator.validate:    {duration_compiled:.4f}s")
    print(f"  Speedup: {speedup:.2f}x")


if __name__ == "__main__":
    run_benchmark()
