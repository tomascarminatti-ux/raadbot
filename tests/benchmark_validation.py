"""
Benchmark comparing standard jsonschema.validate vs pre-compiled validator.
"""

import json
import time
from jsonschema import validate
from jsonschema.validators import validator_for


def main():
    schema_path = "schemas/gem_output.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    sample_data = {
        "meta": {
            "search_id": "SEARCH-2025-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2025-01-01T00:00:00Z",
            "sources": ["cv.txt"],
        },
        "scores": {"score_dimension": 8, "confidence": 9},
        "blockers": [],
        "content": {"summary": "Benchmark payload"},
    }

    iterations = 1000

    # Standard jsonschema.validate
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate(instance=sample_data, schema=schema)
    t1 = time.perf_counter()
    duration_standard = t1 - t0

    # Pre-compiled validator
    validator_cls = validator_for(schema)
    validator = validator_cls(schema)

    t2 = time.perf_counter()
    for _ in range(iterations):
        validator.validate(sample_data)
    t3 = time.perf_counter()
    duration_compiled = t3 - t2

    speedup = duration_standard / duration_compiled if duration_compiled > 0 else 0

    print(f"Iterations: {iterations}")
    print(f"Standard jsonschema.validate: {duration_standard:.4f}s")
    print(f"Pre-compiled validator:       {duration_compiled:.4f}s")
    print(f"Speedup:                       {speedup:.2f}x")


if __name__ == "__main__":
    main()
