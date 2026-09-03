"""
benchmark_validation.py – Benchmarks schema validation speedup (uncompiled vs compiled jsonschema validator).
"""

import json
import time
from jsonschema import validate
from jsonschema.validators import validator_for


def run_benchmark():
    schema_path = "schemas/gem_output.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    sample = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2026-01-01T00:00:00Z",
            "sources": ["cv.txt"],
        },
        "scores": {"score_dimension": 8, "confidence": 9},
        "blockers": [],
        "content": {"summary": "good"},
    }

    iterations = 2000

    # 1. Uncompiled jsonschema.validate
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate(instance=sample, schema=schema)
    t1 = time.perf_counter()
    time_uncompiled = t1 - t0

    # 2. Precompiled validator instance
    validator_cls = validator_for(schema)
    validator = validator_cls(schema)
    t2 = time.perf_counter()
    for _ in range(iterations):
        validator.validate(instance=sample)
    t3 = time.perf_counter()
    time_compiled = t3 - t2

    speedup = time_uncompiled / time_compiled if time_compiled > 0 else 0
    print(f"Iterations:   {iterations}")
    print(f"Uncompiled:   {time_uncompiled:.4f} seconds")
    print(f"Precompiled:  {time_compiled:.4f} seconds")
    print(f"Speedup:      {speedup:.2f}x faster")


if __name__ == "__main__":
    run_benchmark()
