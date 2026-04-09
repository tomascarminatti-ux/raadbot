import time
import os
import json
from jsonschema import validate, ValidationError
from jsonschema.validators import validator_for

# Mock data matching the schema
valid_json = {
    "meta": {
        "search_id": "SEARCH-2026-001",
        "candidate_id": "CAND-001",
        "gem": "GEM_1",
        "prompt_version": "v1.2",
        "timestamp": "2026-01-01T12:00:00Z",
        "sources": ["cv.txt"]
    },
    "scores": {
        "score_dimension": 8,
        "confidence": 9
    },
    "blockers": [],
    "content": {
        "summary": "Excellent candidate."
    }
}

def benchmark_validation_optimized(n=1000):
    schema_path = os.path.join("schemas", "gem_output.schema.json")
    with open(schema_path, "r") as f:
        schema = json.load(f)

    # Pre-compile validator
    cls = validator_for(schema)
    cls.check_schema(schema)
    validator = cls(schema)

    print("Starting optimized benchmark...")
    start = time.perf_counter()
    for _ in range(n):
        validator.validate(valid_json)
    end = time.perf_counter()

    duration = end - start
    print(f"Optimized Benchmark: {n} validations took {duration:.4f} seconds")
    print(f"Average time per validation: {duration / n * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark_validation_optimized(1000)
