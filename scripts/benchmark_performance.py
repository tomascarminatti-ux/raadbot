
import time
import os
import sys

# Add the current directory to the path so we can import the agent module
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

def benchmark_build_prompt():
    print("Benchmarking build_prompt...")
    variables = {
        "search_id": "SEARCH-2025-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years in Python.",
        "interview_notes": "Strong technical skills, good communication.",
        "gem5_summary": "Strategic role for a fintech company."
    }

    # Warm up
    build_prompt("gem1", variables)

    start_time = time.perf_counter()
    iterations = 100
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time*1000:.4f} ms")

def benchmark_validation():
    print("\nBenchmarking jsonschema validation...")
    from jsonschema import validate
    import json

    schema_path = "schemas/gem_output.schema.json"
    with open(schema_path, "r") as f:
        schema = json.load(f)

    sample_output = {
        "meta": {
            "search_id": "SEARCH-2025-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2025-01-01T12:00:00Z",
            "sources": ["cv.txt"]
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9
        },
        "blockers": [],
        "content": {"test": "data"}
    }

    # Warm up
    validate(instance=sample_output, schema=schema)

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        validate(instance=sample_output, schema=schema)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for jsonschema.validate: {avg_time*1000:.4f} ms")

    from jsonschema.validators import validator_for
    validator_cls = validator_for(schema)
    validator = validator_cls(schema)

    # Warm up
    validator.validate(sample_output)

    start_time = time.perf_counter()
    for _ in range(iterations):
        validator.validate(sample_output)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for pre-compiled validator: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark_build_prompt()
    benchmark_validation()
