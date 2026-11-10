"""
benchmark_validation.py – Benchmark comparing uncompiled jsonschema.validate vs pre-compiled validator.
"""

import json
import timeit
from jsonschema import validate
from jsonschema.validators import validator_for


def run_benchmark():
    with open("schemas/gem_output.schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)

    validator_cls = validator_for(schema)
    validator = validator_cls(schema)

    sample_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["brief_jd.txt"],
        },
        "scores": {"score_dimension": 8, "confidence": 9},
        "blockers": [],
        "content": {"summary": "Valid candidate summary."},
    }

    n_iterations = 1000
    t_uncompiled = timeit.timeit(
        lambda: validate(instance=sample_data, schema=schema), number=n_iterations
    )
    t_compiled = timeit.timeit(
        lambda: validator.validate(sample_data), number=n_iterations
    )

    print(f"Benchmark: {n_iterations} schema validations")
    print(f"  Uncompiled jsonschema.validate: {t_uncompiled:.4f}s ({t_uncompiled / n_iterations * 1000:.3f}ms/op)")
    print(f"  Pre-compiled validator.validate: {t_compiled:.4f}s ({t_compiled / n_iterations * 1000:.3f}ms/op)")
    print(f"  Speedup: {t_uncompiled / t_compiled:.2f}x")


if __name__ == "__main__":
    run_benchmark()
