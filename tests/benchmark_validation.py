import json
import os
import time
import jsonschema
from jsonschema.validators import validator_for

def main():
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # Dummy JSON data that passes validation
    sample_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["brief_jd.txt"]
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9
        },
        "blockers": [],
        "content": {
            "problema_real_del_rol": "Test challenge"
        }
    }

    iterations = 2000

    # 1. Standard Validation (Compiles on every call)
    t0 = time.perf_counter()
    for _ in range(iterations):
        jsonschema.validate(instance=sample_data, schema=schema)
    t1 = time.perf_counter()
    standard_duration = t1 - t0

    # 2. Precompiled Validation
    t2 = time.perf_counter()
    validator_class = validator_for(schema)
    validator = validator_class(schema)
    for _ in range(iterations):
        validator.validate(sample_data)
    t3 = time.perf_counter()
    compiled_duration = t3 - t2

    print(f"--- JSON Schema Validation Benchmark ({iterations} iterations) ---")
    print(f"Standard jsonschema.validate duration: {standard_duration:.4f} seconds")
    print(f"Precompiled validator duration:        {compiled_duration:.4f} seconds")
    speedup = standard_duration / compiled_duration if compiled_duration > 0 else float('inf')
    print(f"Precompiled speedup factor:            {speedup:.2f}x faster")

if __name__ == "__main__":
    main()
