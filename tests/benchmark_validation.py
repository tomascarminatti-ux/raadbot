import json
import timeit
import os
from jsonschema import validate
from jsonschema.validators import validator_for


def main():
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_5",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["brief_jd.txt"],
        },
        "scores": {"confidence": 9},
        "blockers": [],
        "content": {"problema_real_del_rol": "Test challenge"},
    }

    # Dynamic validation (creates and compiles validator on every call)
    def run_dynamic():
        validate(instance=data, schema=schema)

    # Pre-compiled validator
    validator = validator_for(schema)(schema)

    def run_precompiled():
        validator.validate(data)

    iterations = 2000
    print(f"Running validation benchmark with {iterations} iterations...")

    t1 = timeit.timeit(run_dynamic, number=iterations)
    t2 = timeit.timeit(run_precompiled, number=iterations)

    print(f"Dynamic validation:   {t1:.4f}s")
    print(f"Precompiled validation: {t2:.4f}s")
    print(f"Speedup: {t1 / t2:.2f}x")


if __name__ == "__main__":
    main()
