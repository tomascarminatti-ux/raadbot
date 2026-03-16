
import time
import json
import os
import functools
from agent.prompt_builder import build_prompt
from jsonschema import validate, Draft7Validator

# Mocking the load_prompt to simulate original behavior vs cached behavior
import agent.prompt_builder as pb

original_load_prompt = pb.load_prompt
original_load_maestro = pb.load_maestro

@functools.lru_cache(maxsize=32)
def cached_load_prompt(gem_name: str) -> str:
    return original_load_prompt(gem_name)

@functools.lru_cache(maxsize=1)
def cached_load_maestro() -> str:
    return original_load_maestro()

def benchmark_prompt_builder():
    variables = {
        "search_id": "SEARCH-2024-001",
        "candidate_id": "CAND-001",
        "cv_text": "Sample CV content",
        "interview_notes": "Sample notes",
        "gem5_summary": "Sample summary"
    }

    print("--- Prompt Builder Benchmark ---")
    # Original
    start = time.perf_counter()
    for _ in range(1000):
        build_prompt("gem1", variables)
    end = time.perf_counter()
    print(f"Time to build 1000 prompts (original): {end - start:.4f}s")

    # Patch for caching
    pb.load_prompt = cached_load_prompt
    pb.load_maestro = cached_load_maestro

    # Warm up cache
    build_prompt("gem1", variables)

    start = time.perf_counter()
    for _ in range(1000):
        build_prompt("gem1", variables)
    end = time.perf_counter()
    print(f"Time to build 1000 prompts (cached): {end - start:.4f}s")

def benchmark_validation():
    schema_path = os.path.join("schemas", "gem_output.schema.json")
    with open(schema_path, "r") as f:
        schema = json.load(f)

    sample_data = {
        "meta": {
            "search_id": "SEARCH-2024-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["cv"]
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9
        },
        "blockers": [],
        "content": {}
    }

    print("\n--- JSON Schema Validation Benchmark ---")
    start = time.perf_counter()
    for _ in range(1000):
        validate(instance=sample_data, schema=schema)
    end = time.perf_counter()
    print(f"Time for 1000 validations (jsonschema.validate): {end - start:.4f}s")

    validator = Draft7Validator(schema)
    start = time.perf_counter()
    for _ in range(1000):
        validator.validate(instance=sample_data)
    end = time.perf_counter()
    print(f"Time for 1000 validations (Draft7Validator - Pre-compiled): {end - start:.4f}s")

if __name__ == "__main__":
    benchmark_prompt_builder()
    benchmark_validation()
