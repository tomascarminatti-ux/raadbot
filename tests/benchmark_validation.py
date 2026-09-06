import json
import os
import time
from jsonschema import validate
from jsonschema.validators import validator_for


def run_benchmark(iterations: int = 2000):
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    dummy_json = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2026-01-01T00:00:00Z",
            "sources": ["cv.txt"],
        },
        "scores": {"score_dimension": 8, "confidence": 9},
        "blockers": [],
        "content": {},
    }

    # 1. Standard validate()
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate(instance=dummy_json, schema=schema)
    t1 = time.perf_counter()
    standard_time = t1 - t0

    # 2. Compiled validator
    validator_cls = validator_for(schema)
    validator = validator_cls(schema)

    t2 = time.perf_counter()
    for _ in range(iterations):
        validator.validate(dummy_json)
    t3 = time.perf_counter()
    compiled_time = t3 - t2

    speedup = standard_time / compiled_time if compiled_time > 0 else 0

    print(f"Standard jsonschema.validate: {standard_time:.4f}s ({iterations} iterations)")
    print(f"Precompiled validator:       {compiled_time:.4f}s ({iterations} iterations)")
    print(f"Speedup:                       {speedup:.2f}x faster")

    assert speedup > 2.0, "Compiled validator should be at least 2x faster"


if __name__ == "__main__":
    run_benchmark()
