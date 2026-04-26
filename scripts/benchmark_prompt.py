import os
import time
import sys
import statistics
from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=100):
    variables = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years in Python.",
        "interview_notes": "Great communication skills, strong technical background.",
        "gem5_summary": "Summary of GEM5 analysis.",
        "gem5_key_challenge": "Implementing scalable microservices."
    }

    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        build_prompt("gem1", variables)
        end = time.perf_counter()
        times.append(end - start)

    avg_time = statistics.mean(times)
    std_dev = statistics.stdev(times)
    print(f"Average time to build prompt (gem1): {avg_time*1000:.4f} ms")
    print(f"Standard deviation: {std_dev*1000:.4f} ms")
    print(f"Max time: {max(times)*1000:.4f} ms")
    print(f"Min time: {min(times)*1000:.4f} ms")

if __name__ == "__main__":
    benchmark_build_prompt()
