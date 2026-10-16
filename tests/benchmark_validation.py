"""
benchmark_validation.py – Benchmark measuring JSON schema validation optimization.
"""

import json
import time
from jsonschema import validate
from jsonschema.validators import validator_for


def run_benchmark():
    schema_path = "schemas/gem_output.schema.json"
    example_path = "templates/output_example.json"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    with open(example_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    iterations = 1000

    # Benchmark uncompiled jsonschema.validate
    start = time.perf_counter()
    for _ in range(iterations):
        validate(instance=data, schema=schema)
    t_uncompiled = time.perf_counter() - start

    # Benchmark pre-compiled validator
    validator = validator_for(schema)(schema)
    start = time.perf_counter()
    for _ in range(iterations):
        validator.validate(data)
    t_compiled = time.perf_counter() - start

    speedup = t_uncompiled / t_compiled if t_compiled > 0 else float("inf")

    print(f"Iterations: {iterations}")
    print(f"Uncompiled jsonschema.validate: {t_uncompiled:.4f} seconds")
    print(f"Pre-compiled validator.validate: {t_compiled:.4f} seconds")
    print(f"Speedup: {speedup:.2f}x")


if __name__ == "__main__":
    run_benchmark()
