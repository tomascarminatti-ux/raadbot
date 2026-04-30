import time
import os
import sys

# Ensure agent package is findable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "TEST-SEARCH",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years of experience in Python and cloud architecture.",
        "interview_notes": "Strong technical skills, good communication.",
        "gem5_summary": "Role requires deep expertise in distributed systems.",
        "gem5_key_challenge": "Scaling the data ingestion pipeline."
    }

    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_latency = (end_time - start_time) / iterations * 1000
    print(f"Average latency for build_prompt: {avg_latency:.4f} ms")

if __name__ == "__main__":
    benchmark()
