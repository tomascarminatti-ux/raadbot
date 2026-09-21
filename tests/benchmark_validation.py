"""
benchmark_validation.py – Benchmark comparing standard jsonschema.validate against precompiled validator.
"""

import json
import time
from jsonschema import validate
import jsonschema.validators


def run_benchmark(iterations: int = 2000):
    schema_path = "schemas/gem_output.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    sample_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["s1"],
        },
        "scores": {"score_dimension": 8, "confidence": 9},
        "blockers": [],
        "content": {},
    }

    # 1. Uncompiled standard validate()
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate(instance=sample_data, schema=schema)
    t1 = time.perf_counter()
    standard_time = t1 - t0

    # 2. Precompiled validator
    validator_cls = jsonschema.validators.validator_for(schema)
    validator = validator_cls(schema)

    t2 = time.perf_counter()
    for _ in range(iterations):
        validator.validate(sample_data)
    t3 = time.perf_counter()
    compiled_time = t3 - t2

    speedup = standard_time / compiled_time if compiled_time > 0 else 0

    print(f"Iterations: {iterations}")
    print(f"Standard jsonschema.validate: {standard_time:.4f}s")
    print(f"Precompiled validator:       {compiled_time:.4f}s")
    print(f"Speedup:                    {speedup:.2f}x")

    return standard_time, compiled_time, speedup


if __name__ == "__main__":
    run_benchmark()
