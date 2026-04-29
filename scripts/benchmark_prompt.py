import time
import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=1000):
    gem_name = "gem1"
    variables = {
        "search_id": "TEST-SEARCH",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years in Python.",
        "interview_notes": "Good communication skills, strong technical background.",
        "gem5_summary": "Search for a Senior Python Developer."
    }

    # Warm up
    build_prompt(gem_name, variables)

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt(gem_name, variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark_build_prompt()
