import time
import json
import os
from jsonschema import validate
from jsonschema.validators import validator_for

def main():
    schema_path = os.path.join(os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    validator_cls = validator_for(schema)
    validator_cls.check_schema(schema)
    precompiled_validator = validator_cls(schema)

    sample_json = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2026-01-01T00:00:00Z",
            "sources": ["brief_jd.txt"]
        },
        "scores": {"confidence": 9, "score_dimension": 8},
        "blockers": [],
        "content": {"summary": "Candidate evaluation sample"}
    }

    iterations = 2000

    # Uncompiled validation
    start = time.perf_counter()
    for _ in range(iterations):
        validate(instance=sample_json, schema=schema)
    uncompiled_time = time.perf_counter() - start

    # Precompiled validation
    start = time.perf_counter()
    for _ in range(iterations):
        precompiled_validator.validate(sample_json)
    precompiled_time = time.perf_counter() - start

    speedup = uncompiled_time / precompiled_time if precompiled_time > 0 else 0.0

    print(f"Benchmark results ({iterations} iterations):")
    print(f"  Uncompiled jsonschema.validate: {uncompiled_time:.4f} seconds")
    print(f"  Precompiled validator.validate: {precompiled_time:.4f} seconds")
    print(f"  Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    main()
