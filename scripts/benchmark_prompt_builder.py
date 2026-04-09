import time
import os
import sys
from agent.prompt_builder import build_prompt

# Mock variables
variables = {
    "search_id": "SEARCH-001",
    "candidate_id": "CAND-001",
    "cv_text": "Experienced software engineer...",
    "interview_notes": "Great technical skills.",
    "gem5_summary": "Strategic role in a fast-paced environment.",
    "jd_text": "Looking for a Senior Developer.",
    "kickoff_notes": "Priority on scalability.",
    "company_context": "Tech startup.",
    "problema_real_del_rol": "Scale the platform to 1M users.",
    "gem1": "Result of GEM1",
    "gem2": "Result of GEM2",
    "gem3": "Result of GEM3",
    "sources_index": "cv_text, interview_notes",
    "tests_text": "Passed all tests.",
    "case_notes": "Strong problem solving.",
    "references_text": "Highly recommended.",
    "client_culture": "Agile and collaborative."
}

def benchmark(n=100):
    start = time.perf_counter()
    for _ in range(n):
        for gem in ["gem1", "gem2", "gem3", "gem4", "gem5"]:
            try:
                build_prompt(gem, variables)
            except FileNotFoundError:
                pass
    end = time.perf_counter()
    duration = end - start
    print(f"Benchmark: {n * 5} prompt builds took {duration:.4f} seconds")
    print(f"Average time per build: {duration / (n * 5) * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark(200)
