import time
import json
from jsonschema import validate
from jsonschema.validators import validator_for


def run_benchmark():
    schema_path = "schemas/gem_output.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    test_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["s1"],
        },
        "scores": {"score_dimension": 4, "confidence": 8},
        "blockers": [],
        "content": {},
    }

    iterations = 2000

    # 1. Uncompiled standard validate
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate(instance=test_data, schema=schema)
    t1 = time.perf_counter()
    uncompiled_time = t1 - t0

    # 2. Precompiled validator
    t0 = time.perf_counter()
    val_cls = validator_for(schema)
    validator = val_cls(schema)
    for _ in range(iterations):
        validator.validate(test_data)
    t1 = time.perf_counter()
    compiled_time = t1 - t0

    print(f"Iterations: {iterations}")
    print(f"Uncompiled Standard jsonschema.validate time: {uncompiled_time:.4f}s")
    print(
        f"Compiled Validator jsonschema.I_VALIDATOR.validate time: {compiled_time:.4f}s"
    )
    print(f"Speedup: {uncompiled_time / compiled_time:.2f}x")


if __name__ == "__main__":
    run_benchmark()
