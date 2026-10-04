"""
benchmark_validation.py – Benchmark para comparar validación JSON Schema directa vs pre-compilada.
"""

import json
import time
from jsonschema import validate
from jsonschema.validators import validator_for


def main():
    with open("schemas/gem_output.schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)

    sample_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2026-01-01T00:00:00Z",
            "sources": ["cv.txt"],
        },
        "scores": {"score_dimension": 8, "confidence": 9},
        "blockers": [],
        "content": {"summary": "Candidato idóneo con fuerte experiencia"},
    }

    iterations = 1000

    # 1. Sin pre-compilar
    start = time.perf_counter()
    for _ in range(iterations):
        validate(instance=sample_data, schema=schema)
    uncompiled_time = time.perf_counter() - start

    # 2. Pre-compilado (Pipeline approach)
    ValidatorCls = validator_for(schema)
    validator = ValidatorCls(schema)
    start = time.perf_counter()
    for _ in range(iterations):
        validator.validate(sample_data)
    compiled_time = time.perf_counter() - start

    speedup = uncompiled_time / compiled_time if compiled_time > 0 else float("inf")

    print(f"=== Benchmark JSON Schema Validation ({iterations} iteraciones) ===")
    print(f"Sin pre-compilar (jsonschema.validate): {uncompiled_time:.4f}s")
    print(f"Pre-compilado (validator.validate):      {compiled_time:.4f}s")
    print(f"Speedup:                                {speedup:.1f}x")


if __name__ == "__main__":
    main()
