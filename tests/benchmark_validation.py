import json
import time
import os
import jsonschema
from jsonschema.validators import validator_for

def run_benchmark():
    schema_path = os.path.join(os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # Sample valid data
    data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["cv.txt"]
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9
        },
        "blockers": [],
        "content": {"test": "data"}
    }

    iterations = 2000
    print(f"Running validation benchmark with {iterations} iterations...")

    # 1. Uncompiled validation
    t0 = time.perf_counter()
    for _ in range(iterations):
        jsonschema.validate(instance=data, schema=schema)
    t1 = time.perf_counter()
    uncompiled_time = t1 - t0
    print(f"Uncompiled validate took: {uncompiled_time:.4f} seconds")

    # 2. Compiled validation
    cls = validator_for(schema)
    validator = cls(schema)
    t2 = time.perf_counter()
    for _ in range(iterations):
        validator.validate(data)
    t3 = time.perf_counter()
    compiled_time = t3 - t2
    print(f"Compiled validate took: {compiled_time:.4f} seconds")

    speedup = uncompiled_time / compiled_time
    print(f"Speedup: {speedup:.2f}x faster!")

if __name__ == "__main__":
    run_benchmark()
