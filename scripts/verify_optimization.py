import time
import os
import sys
import json
from jsonschema import validate

# Add the current directory to sys.path
sys.path.append(os.getcwd())

def benchmark_validation():
    schema_path = "schemas/gem_output.schema.json"
    with open(schema_path, "r") as f:
        schema = json.load(f)

    sample_output = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "candidate_id": "CAND-001",
            "prompt_version": "v1.0",
            "timestamp": "2024-05-20T10:00:00Z",
            "sources": ["CV"]
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9
        },
        "blockers": [],
        "content": {"some": "data"}
    }

    # Warm up
    for _ in range(5):
        try:
            validate(instance=sample_output, schema=schema)
        except Exception as e:
            print(f"Validation error during warm up: {e}")
            import traceback
            traceback.print_exc()
            return

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        validate(instance=sample_output, schema=schema)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for jsonschema.validate: {avg_time*1000:.4f} ms")

    # Now test with pre-compiled validator
    from jsonschema.validators import validator_for
    validator_cls = validator_for(schema)
    validator = validator_cls(schema)

    # Warm up
    for _ in range(5):
        validator.validate(sample_output)

    start_time = time.perf_counter()
    for _ in range(iterations):
        validator.validate(sample_output)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for pre-compiled validator: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark_validation()
