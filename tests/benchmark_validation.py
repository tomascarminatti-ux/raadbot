"""
Benchmark comparing jsonschema.validate vs compiled validator.
"""

import time
import json
from jsonschema import validate, validators

def run_benchmark():
    schema_path = "schemas/gem_output.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    with open("templates/output_example.json", "r", encoding="utf-8") as f:
        sample_data = json.load(f)

    iterations = 1000

    # Uncompiled: validate(instance, schema)
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate(instance=sample_data, schema=schema)
    t1 = time.perf_counter()
    time_uncompiled = (t1 - t0) * 1000

    # Compiled: validator_for(schema)(schema).validate(instance)
    validator_cls = validators.validator_for(schema)
    validator = validator_cls(schema)

    t2 = time.perf_counter()
    for _ in range(iterations):
        validator.validate(sample_data)
    t3 = time.perf_counter()
    time_compiled = (t3 - t2) * 1000

    speedup = time_uncompiled / time_compiled
    print(f"Iterations: {iterations}")
    print(f"Uncompiled validate(): {time_uncompiled:.2f} ms ({time_uncompiled/iterations:.4f} ms/call)")
    print(f"Pre-compiled validator.validate(): {time_compiled:.2f} ms ({time_compiled/iterations:.4f} ms/call)")
    print(f"Speedup: {speedup:.2f}x faster")

if __name__ == "__main__":
    run_benchmark()
