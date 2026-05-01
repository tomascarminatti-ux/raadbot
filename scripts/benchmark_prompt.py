import time
import os
import sys

# Ensure project root is in sys.path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "test-search",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years of experience in Python and Cloud.",
        "interview_notes": "Great candidate, strong technical skills.",
        "gem5_summary": {"role": "Lead Engineer", "company": "Tech Corp"},
    }

    # Warm up
    build_prompt("gem1", variables)

    start = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end = time.perf_counter()

    avg_time = (end - start) / iterations
    print(f"Average time per build_prompt: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
