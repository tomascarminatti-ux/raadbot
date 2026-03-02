import time
import os
import sys
sys.path.append(os.getcwd())
from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "SEARCH-123",
        "candidate_id": "CAND-456",
        "cv_text": "Experienced software engineer with 10 years in Python and AI.",
        "interview_notes": "Strong technical skills, good communication.",
        "gem5_summary": "Looking for a tech lead for a new AI project.",
        "gem1": {"some": "data"},
        "gem2": {"more": "data"},
        "gem3": {"even": "more"},
        "sources_index": "cv, interview"
    }

    # Warmup
    for _ in range(10):
        build_prompt("gem4", variables)

    start = time.perf_counter()
    n = 100
    for _ in range(n):
        build_prompt("gem4", variables)
    end = time.perf_counter()

    avg_time = (end - start) / n
    print(f"Average time to build prompt: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
