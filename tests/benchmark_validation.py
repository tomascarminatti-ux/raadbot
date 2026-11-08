"""Benchmark script measuring jsonschema precompiled validation vs default validate."""

import json
import time
from jsonschema import validate
from jsonschema.validators import validator_for

def run_benchmark(iterations: int = 1000):
    with open("schemas/gem_output.schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)

    data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["cv.txt"],
        },
        "scores": {"score_dimension": 8, "confidence": 8},
        "blockers": [],
        "content": {"test": "data"},
    }

    # Warmup
    validate(instance=data, schema=schema)
    validator_cls = validator_for(schema)
    validator = validator_cls(schema)
    validator.validate(data)

    # Benchmark default jsonschema.validate()
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate(instance=data, schema=schema)
    t1 = time.perf_counter()

    # Benchmark pre-compiled validator.validate()
    t2 = time.perf_counter()
    for _ in range(iterations):
        validator.validate(data)
    t3 = time.perf_counter()

    time_default = t1 - t0
    time_compiled = t3 - t2
    speedup = time_default / time_compiled

    print(f"Iterations: {iterations}")
    print(f"jsonschema.validate (uncompiled):   {time_default:.4f}s ({(time_default / iterations) * 1000:.3f} ms/call)")
    print(f"validator.validate (precompiled):    {time_compiled:.4f}s ({(time_compiled / iterations) * 1000:.3f} ms/call)")
    print(f"Speedup: {speedup:.2f}x faster")

if __name__ == "__main__":
    run_benchmark()
