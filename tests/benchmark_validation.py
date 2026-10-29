import json
import time
import jsonschema
from jsonschema.validators import validator_for

def benchmark():
    with open("schemas/gem_output.schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)

    data = {
        "meta": {
            "search_id": "SEARCH-2024-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2025-01-01T00:00:00Z",
            "sources": ["cv_text"]
        },
        "scores": {"confidence": 8, "score_dimension": 8},
        "blockers": [],
        "content": {"test": "data"}
    }

    iterations = 1000

    # Uncompiled jsonschema.validate
    t0 = time.perf_counter()
    for _ in range(iterations):
        jsonschema.validate(instance=data, schema=schema)
    t1 = time.perf_counter()
    uncompiled_time = t1 - t0

    # Pre-compiled validator instance
    validator_cls = validator_for(schema)
    validator = validator_cls(schema)

    t0 = time.perf_counter()
    for _ in range(iterations):
        validator.validate(data)
    t1 = time.perf_counter()
    compiled_time = t1 - t0

    speedup = uncompiled_time / compiled_time if compiled_time > 0 else float("inf")

    print("=== JSON Schema Validation Benchmark ===")
    print(f"Iterations: {iterations}")
    print(f"Uncompiled validation time: {uncompiled_time:.4f}s ({uncompiled_time / iterations * 1000:.4f} ms/op)")
    print(f"Compiled validation time:   {compiled_time:.4f}s ({compiled_time / iterations * 1000:.4f} ms/op)")
    print(f"Speedup:                    {speedup:.2f}x faster")

if __name__ == "__main__":
    benchmark()
