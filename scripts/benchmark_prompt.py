import time
import sys
import os

# Add root to sys.path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "TEST-123",
        "candidate_id": "CAND-456",
        "cv_text": "Experienced software engineer with 10 years in Python.",
        "interview_notes": "Great communication skills, strong technical background.",
        "gem5_summary": "Role requires high performance and security focus.",
        "VERSION": "1.0.0"
    }

    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time * 1000:.4f} ms")

if __name__ == "__main__":
    try:
        benchmark()
    except Exception as e:
        print(f"Error: {e}")
