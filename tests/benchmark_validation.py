"""
benchmark_validation.py – Measures the performance impact of JSON Schema precompilation.
"""

import json
import timeit
from jsonschema import validate
from jsonschema.validators import validator_for

def main():
    schema_path = "schemas/gem_output.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    test_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["s1"]
        },
        "scores": {
            "confidence": 8,
            "score_dimension": 7
        },
        "content": {},
        "blockers": []
    }

    # Run a single validation for correctness
    validate(test_data, schema)

    val_cls = validator_for(schema)
    validator = val_cls(schema)
    validator.validate(test_data)

    print("--- Starting Benchmark (2,000 iterations) ---")

    # 1. Standard jsonschema.validate
    time_std = timeit.timeit(lambda: validate(test_data, schema), number=2000)
    print(f"Standard validate():  {time_std:.4f} seconds")

    # 2. Precompiled validator.validate
    time_opt = timeit.timeit(lambda: validator.validate(test_data), number=2000)
    print(f"Precompiled validator: {time_opt:.4f} seconds")

    speedup = time_std / time_opt
    print(f"Speedup Factor:        {speedup:.2f}x")
    print("---------------------------------------------")

if __name__ == "__main__":
    main()
