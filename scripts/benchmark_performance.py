import time
import os
import sys
import json
from unittest.mock import MagicMock

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt
from agent.pipeline import Pipeline

def benchmark_prompt_builder(iterations=1000):
    variables = {
        "search_id": "SEARCH-2024-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with a focus on performance.",
        "interview_notes": "Strong technical skills, good communication.",
        "gem5_summary": "Role requires high scalability expertise."
    }

    # Warm up
    build_prompt("gem1", variables)

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Prompt Builder Average Time: {avg_time*1000:.4f} ms")

def benchmark_schema_loading(iterations=100):
    gemini_mock = MagicMock()

    start_time = time.perf_counter()
    for _ in range(iterations):
        p = Pipeline(gemini_mock, "test_search", "test_output")
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Pipeline Initialization (includes schema load) Average Time: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark_prompt_builder()
    benchmark_schema_loading()
