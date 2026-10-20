import json
import time
from jsonschema import validate, ValidationError
from jsonschema.validators import validator_for

def benchmark():
    with open('templates/output_example.json') as f:
        dummy_data = json.load(f)

    with open('schemas/gem_output.schema.json') as f:
        schema = json.load(f)

    # 1. Uncompiled jsonschema.validate
    start = time.perf_counter()
    for _ in range(5000):
        validate(instance=dummy_data, schema=schema)
    uncompiled = time.perf_counter() - start

    # 2. Compiled validator
    val_cls = validator_for(schema)
    validator = val_cls(schema)

    start = time.perf_counter()
    for _ in range(5000):
        validator.validate(dummy_data)
    compiled = time.perf_counter() - start

    print(f"Uncompiled: {uncompiled:.4f}s")
    print(f"Compiled:   {compiled:.4f}s")
    print(f"Speedup:    {uncompiled/compiled:.2f}x")

if __name__ == "__main__":
    benchmark()
