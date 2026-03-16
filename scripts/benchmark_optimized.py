
import time
import json
import os
from agent.prompt_builder import build_prompt
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

def benchmark_prompt_builder():
    variables = {
        "search_id": "SEARCH-2024-001",
        "candidate_id": "CAND-001",
        "cv_text": "Sample CV content",
        "interview_notes": "Sample notes",
        "gem5_summary": "Sample summary"
    }

    print("--- Prompt Builder Benchmark (Optimized) ---")
    # Warm up cache
    build_prompt("gem1", variables)

    start = time.perf_counter()
    for _ in range(1000):
        build_prompt("gem1", variables)
    end = time.perf_counter()
    print(f"Time to build 1000 prompts: {end - start:.4f}s")

def benchmark_validation():
    # Setup Pipeline with dummy client
    pipeline = Pipeline(GeminiClient(api_key="dummy"), "SEARCH-2024-001", "output_test")

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

    print("\n--- JSON Schema Validation Benchmark (Optimized) ---")
    # Warm up
    pipeline._validate_output(sample_data, "gem1")

    start = time.perf_counter()
    for _ in range(1000):
        pipeline._validate_output(sample_data, "gem1")
    end = time.perf_counter()
    print(f"Time for 1000 validations: {end - start:.4f}s")

if __name__ == "__main__":
    benchmark_prompt_builder()
    benchmark_validation()
