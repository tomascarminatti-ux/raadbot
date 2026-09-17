import time
import json
import os
from jsonschema import validate
from jsonschema.validators import validator_for


def run_benchmark():
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    sample_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["cv.txt"],
        },
        "scores": {"score_dimension": 8, "confidence": 9},
        "blockers": [],
        "content": {"summary": "Benchmark candidate summary"},
    }

    iterations = 2000

    # Benchmark uncompiled
    start_uncompiled = time.perf_counter()
    for _ in range(iterations):
        validate(instance=sample_data, schema=schema)
    time_uncompiled = time.perf_counter() - start_uncompiled

    # Benchmark pre-compiled
    validator_cls = validator_for(schema)
    compiled_validator = validator_cls(schema)

    start_compiled = time.perf_counter()
    for _ in range(iterations):
        compiled_validator.validate(sample_data)
    time_compiled = time.perf_counter() - start_compiled

    speedup = time_uncompiled / time_compiled
    print(f"Iterations: {iterations}")
    print(f"Uncompiled jsonschema.validate: {time_uncompiled:.4f}s")
    print(f"Precompiled validator instance: {time_compiled:.4f}s")
    print(f"Speedup: {speedup:.2f}x")


if __name__ == "__main__":
    run_benchmark()
