import time
import os
import sys
import json
import re
import functools
import asyncio
from typing import Optional, Any

# Add root to path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt, load_prompt
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

def benchmark_validation():
    print("\n--- Benchmarking JSON Validation ---")

    # Initialize Pipeline (which now pre-compiles the validator)
    # Mocking GeminiClient to avoid API calls
    class MockGemini:
        pass

    pipeline = Pipeline(gemini=MockGemini(), search_id="test", output_dir="runs/test")

    # Sample valid data for GEM_1
    data = {
        "meta": {
            "search_id": "SEARCH-2024-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2024-05-20T10:00:00Z",
            "sources": ["cv.pdf"]
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9
        },
        "blockers": [],
        "content": {"key": "value"}
    }

    iterations = 5000

    start = time.time()
    for _ in range(iterations):
        pipeline._validate_output(data, "GEM_1")
    duration = time.time() - start
    print(f"Optimized (Pre-compiled): {duration:.4f}s ({duration/iterations*1000:.4f} ms/op)")

def benchmark_prompt_building():
    print("\n--- Benchmarking Prompt Building ---")
    variables = {
        "search_id": "SEARCH-123",
        "candidate_id": "CAND-456",
        "cv_text": "Some long CV text...",
        "interview_notes": "Good notes",
        "gem5_summary": {"complex": "object", "nested": 123}
    }

    iterations = 5000

    # Warm up cache
    try:
        build_prompt("gem1", variables)
    except Exception as e:
        print(f"Skipping actual build_prompt due to missing prompt files: {e}")
        return

    start = time.time()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    duration = time.time() - start
    print(f"Optimized (Cached + Pre-compiled Regex): {duration:.4f}s ({duration/iterations*1000:.4f} ms/op)")

if __name__ == "__main__":
    benchmark_validation()
    benchmark_prompt_building()
