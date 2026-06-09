import time
import os
import sys

# Add current directory to path so we can import agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    gem_name = "gem1"
    variables = {
        "search_id": "TEST-ID",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years of experience in Python and Cloud.",
        "interview_notes": "Good communication skills, strong technical background.",
        "gem5_summary": "Company is looking for a senior lead to drive the new platform."
    }

    # Warm up
    for _ in range(10):
        build_prompt(gem_name, variables)

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt(gem_name, variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time per build_prompt call: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    try:
        benchmark()
    except Exception as e:
        print(f"Error during benchmark: {e}")
