import time
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.prompt_builder import build_prompt
from agent.pipeline import Pipeline, _load_schema_cached
from unittest.mock import MagicMock

def benchmark_prompt_builder(iterations=1000):
    variables = {
        "search_id": "TEST-SEARCH",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with a background in Python and cloud computing.",
        "interview_notes": "Strong technical skills, good communicator.",
        "gem5_summary": "Company is looking for a senior lead."
    }

    # Warm up cache
    build_prompt("gem1", variables)

    start_time = time.time()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt over {iterations} iterations: {avg_time:.6f} seconds")

def benchmark_schema_loading(iterations=1000):
    # Warm up cache
    _load_schema_cached()

    start_time = time.time()
    for _ in range(iterations):
        _load_schema_cached()
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for _load_schema_cached over {iterations} iterations: {avg_time:.6f} seconds")

if __name__ == "__main__":
    print("Benchmarking optimized performance...")
    benchmark_prompt_builder()
    benchmark_schema_loading()
