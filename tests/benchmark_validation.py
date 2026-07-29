import os
import json
import time
from jsonschema import validate, ValidationError
from jsonschema.validators import validator_for

def run_benchmark():
    # Load schema
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # Valid mock data
    mock_data = {
        "meta": {
            "search_id": "SEARCH-2024-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["cv_text"]
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9
        },
        "blockers": [],
        "content": {
            "key_achievements": ["achievement 1"]
        }
    }

    iterations = 2000
    print(f"Running JSON schema validation benchmark ({iterations} iterations)...")

    # 1. Benchmark standard validate
    start_time = time.perf_counter()
    for _ in range(iterations):
        validate(instance=mock_data, schema=schema)
    duration_standard = time.perf_counter() - start_time
    print(f"Standard jsonschema.validate: {duration_standard:.4f} seconds")

    # 2. Benchmark pre-compiled validator
    validator_cls = validator_for(schema)
    validator = validator_cls(schema)

    start_time = time.perf_counter()
    for _ in range(iterations):
        validator.validate(mock_data)
    duration_precompiled = time.perf_counter() - start_time
    print(f"Pre-compiled validator:       {duration_precompiled:.4f} seconds")

    # Calculate speedup
    speedup = duration_standard / duration_precompiled
    print(f"⚡ Speedup factor:            {speedup:.2f}x faster!")
    print("-" * 50)

if __name__ == "__main__":
    run_benchmark()
