import json
import timeit
import os
from jsonschema import validate
from jsonschema.validators import validator_for


def run_benchmark():
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    validator_cls = validator_for(schema)
    validator = validator_cls(schema)

    sample_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["cv.txt"],
        },
        "scores": {"score_dimension": 8, "confidence": 9},
        "blockers": [],
        "content": {},
    }

    def dynamic_validate():
        validate(instance=sample_data, schema=schema)

    def compiled_validate():
        validator.validate(sample_data)

    print("Running JSON Schema validation benchmark...")
    iterations = 2000
    t_dynamic = timeit.timeit(dynamic_validate, number=iterations)
    t_compiled = timeit.timeit(compiled_validate, number=iterations)

    print(f"Iterations: {iterations}")
    print(f"Dynamic validation: {t_dynamic:.4f} seconds")
    print(f"Compiled validation: {t_compiled:.4f} seconds")
    speedup = t_dynamic / t_compiled
    print(f"Speedup: {speedup:.2f}x faster!")


if __name__ == "__main__":
    run_benchmark()
