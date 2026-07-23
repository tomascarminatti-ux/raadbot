import time
import os
import json
from jsonschema import validate, ValidationError, validators
from agent.prompt_builder import build_prompt, load_prompt, load_maestro

def benchmark_prompt_loading():
    print("=== Benchmarking Prompt Loading ===")

    # 1. Standard loading (without cache)
    start_time = time.perf_counter()
    for _ in range(1000):
        # We simulate what build_prompt does
        maestro = load_maestro()
        prompt = load_prompt("gem1")
        prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)
    end_time = time.perf_counter()
    without_cache_duration = end_time - start_time
    print(f"Without cache (1000 iterations): {without_cache_duration:.4f} seconds")

    # Now let's try with a simulated manual memory cache
    cache = {}
    def load_prompt_cached(gem_name: str) -> str:
        if gem_name not in cache:
            cache[gem_name] = load_prompt(gem_name)
        return cache[gem_name]

    start_time = time.perf_counter()
    for _ in range(1000):
        maestro = load_prompt_cached("00_prompt_maestro")
        prompt = load_prompt_cached("gem1")
        prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)
    end_time = time.perf_counter()
    with_cache_duration = end_time - start_time
    print(f"With cache (1000 iterations): {with_cache_duration:.4f} seconds")
    print(f"Prompt Loading Speedup: {without_cache_duration / with_cache_duration:.2f}x")


def benchmark_schema_validation():
    print("\n=== Benchmarking Schema Validation ===")

    # Load schema
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    sample_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["cv.txt"]
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9
        },
        "blockers": [],
        "content": {
            "key": "value"
        }
    }

    # 1. Standard validation
    start_time = time.perf_counter()
    for _ in range(2000):
        validate(instance=sample_data, schema=schema)
    end_time = time.perf_counter()
    standard_duration = end_time - start_time
    print(f"Standard jsonschema.validate (2000 iterations): {standard_duration:.4f} seconds")

    # 2. Pre-compiled validation
    validator_class = validators.validator_for(schema)
    # Compile the schema
    validator = validator_class(schema)

    start_time = time.perf_counter()
    for _ in range(2000):
        validator.validate(sample_data)
    end_time = time.perf_counter()
    compiled_duration = end_time - start_time
    print(f"Pre-compiled jsonschema.validate (2000 iterations): {compiled_duration:.4f} seconds")
    print(f"Schema Validation Speedup: {standard_duration / compiled_duration:.2f}x")

if __name__ == "__main__":
    benchmark_prompt_loading()
    benchmark_schema_validation()
