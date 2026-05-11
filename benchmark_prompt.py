import time
import os
from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "test_search",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years of Python.",
        "interview_notes": "Good communication skills.",
        "gem5_summary": "Summary of the role."
    }

    # Warm up (if any caching was already there, which isn't)
    build_prompt("gem1", variables)

    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time per build_prompt call: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
