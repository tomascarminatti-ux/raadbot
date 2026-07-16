import time
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=1000):
    variables = {
        "search_id": "test-search",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years of experience in Python and Cloud.",
        "interview_notes": "Strong technical skills, good communication.",
        "gem5_summary": "Role requires a senior leader with technical depth.",
        "jd_text": "Looking for a Senior Python Developer.",
        "kickoff_notes": "Budget is flexible for the right candidate.",
        "company_context": "Fast-growing AI startup.",
        "client_culture": "Results-oriented, fast-paced.",
    }

    # Warm up
    build_prompt("gem1", variables)

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time to build prompt (gem1): {avg_time * 1000:.4f} ms")
    return avg_time

if __name__ == "__main__":
    benchmark_build_prompt()
