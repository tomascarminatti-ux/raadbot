"""
tests/benchmark_perf.py – Benchmark script for verifying prompt builder and jsonschema validator performance optimizations.
"""

import os
import time
import json
import functools
import jsonschema
from agent.prompt_builder import build_prompt, load_prompt, clear_prompt_caches
from agent.pipeline import _get_validator


def benchmark_prompt_builder():
    print("--- ⚡ Benchmarking Prompt Builder Optimization ⚡ ---")

    variables = {
        "search_id": "SEARCH-2026",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years of Python.",
        "interview_notes": "Great communications and solid system design skills.",
        "gem5_summary": "CEO search for tech company.",
    }

    # 1. Measure baseline simulation (clearing cache every iteration to simulate disk read + re-parsing)
    start_time = time.perf_counter()
    iterations = 500
    for _ in range(iterations):
        clear_prompt_caches()
        build_prompt("gem1", variables)
    end_time = time.perf_counter()
    baseline_avg_ms = ((end_time - start_time) / iterations) * 1000
    print(f"Uncached (Baseline) avg build_prompt: {baseline_avg_ms:.4f} ms")

    # 2. Measure optimized execution (utilizing LRU cache + single-pass re.sub)
    # Warm up first
    build_prompt("gem1", variables)

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()
    optimized_avg_ms = ((end_time - start_time) / iterations) * 1000
    print(f"Optimized (LRU Cached + Single-pass) avg build_prompt: {optimized_avg_ms:.4f} ms")

    speedup = baseline_avg_ms / optimized_avg_ms if optimized_avg_ms > 0 else float('inf')
    print(f"⚡ Prompt Builder Speedup: {speedup:.2f}x faster!\n")


def benchmark_jsonschema():
    print("--- ⚡ Benchmarking JSON Schema Validation Optimization ⚡ ---")

    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    sample_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["brief_jd.txt"]
        },
        "scores": {"confidence": 9, "score_dimension": 8},
        "blockers": [],
        "content": {"problema_real_del_rol": "Test challenge"}
    }

    iterations = 500

    # 1. Uncached / Standard Validation (compiles schema on every single run)
    start_time = time.perf_counter()
    for _ in range(iterations):
        jsonschema.validate(instance=sample_data, schema=schema)
    end_time = time.perf_counter()
    baseline_avg_ms = ((end_time - start_time) / iterations) * 1000
    print(f"Standard (Uncached) avg validation: {baseline_avg_ms:.4f} ms")

    # 2. Optimized Validation (using precompiled validator)
    validator = _get_validator()

    # Warm up
    validator.validate(instance=sample_data)

    start_time = time.perf_counter()
    for _ in range(iterations):
        validator.validate(instance=sample_data)
    end_time = time.perf_counter()
    optimized_avg_ms = ((end_time - start_time) / iterations) * 1000
    print(f"Precompiled (Optimized) avg validation: {optimized_avg_ms:.4f} ms")

    speedup = baseline_avg_ms / optimized_avg_ms if optimized_avg_ms > 0 else float('inf')
    print(f"⚡ JSON Schema Validation Speedup: {speedup:.2f}x faster!\n")


if __name__ == "__main__":
    benchmark_prompt_builder()
    benchmark_jsonschema()
