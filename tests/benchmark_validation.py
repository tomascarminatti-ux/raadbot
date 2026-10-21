"""
benchmark_validation.py – Benchmark script measuring JSON schema validation performance speedup.
"""

import json
import os
import time
from jsonschema import validate, validators


def run_benchmark(iterations: int = 2000):
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    sample_path = os.path.join(
        os.path.dirname(__file__), "..", "templates", "output_example.json"
    )
    with open(sample_path, "r", encoding="utf-8") as f:
        sample_data = json.load(f)

    # 1. Standard uncompiled jsonschema.validate
    start = time.perf_counter()
    for _ in range(iterations):
        validate(instance=sample_data, schema=schema)
    elapsed_uncompiled = time.perf_counter() - start

    # 2. Pre-compiled validator instance
    validator_cls = validators.validator_for(schema)
    validator = validator_cls(schema)

    start = time.perf_counter()
    for _ in range(iterations):
        validator.validate(sample_data)
    elapsed_compiled = time.perf_counter() - start

    speedup = elapsed_uncompiled / elapsed_compiled if elapsed_compiled > 0 else 0

    print("=" * 60)
    print(f"JSON Schema Validation Benchmark ({iterations} iterations)")
    print("=" * 60)
    print(f"Uncompiled jsonschema.validate: {elapsed_uncompiled:.4f}s")
    print(f"Pre-compiled validator.validate: {elapsed_compiled:.4f}s")
    print(f"Speedup: {speedup:.2f}x faster")
    print("=" * 60)

    return speedup


if __name__ == "__main__":
    run_benchmark()
