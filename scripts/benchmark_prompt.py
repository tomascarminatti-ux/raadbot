import time
import os
import sys

# Add the root directory to sys.path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    # Variables for gem1 (based on agent/pipeline.py)
    variables = {
        "search_id": "test_search",
        "candidate_id": "test_candidate",
        "cv_text": "Experienced software engineer with 10 years of experience in Python and AI.",
        "interview_notes": "Strong technical skills, good communication.",
        "gem5_summary": "Searching for a lead engineer for a fintech startup."
    }

    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
