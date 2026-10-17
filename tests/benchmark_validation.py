import time
import json
import jsonschema
from jsonschema.validators import validator_for


def run_benchmark():
    schema_path = "schemas/gem_output.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    test_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_5",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["s1"],
        },
        "scores": {"confidence": 8},
        "blockers": [],
        "content": {},
    }

    iterations = 1000

    # Benchmark 1: Uncompiled jsonschema.validate
    t0 = time.perf_counter()
    for _ in range(iterations):
        jsonschema.validate(instance=test_data, schema=schema)
    t1 = time.perf_counter()
    uncompiled_time = t1 - t0

    # Benchmark 2: Pre-compiled validator instance
    validator_cls = validator_for(schema)
    validator = validator_cls(schema)

    t2 = time.perf_counter()
    for _ in range(iterations):
        validator.validate(test_data)
    t3 = time.perf_counter()
    compiled_time = t3 - t2

    speedup = uncompiled_time / compiled_time if compiled_time > 0 else 0

    print(f"--- Benchmark JSON Schema Validation ({iterations} iterations) ---")
    print(f"Uncompiled jsonschema.validate: {uncompiled_time:.4f} seconds")
    print(f"Pre-compiled validator.validate: {compiled_time:.4f} seconds")
    print(f"Speedup: {speedup:.2f}x")

    return uncompiled_time, compiled_time, speedup


if __name__ == "__main__":
    run_benchmark()
