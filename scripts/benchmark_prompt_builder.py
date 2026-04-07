import time
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years in Python and cloud architecture.",
        "interview_notes": "Strong technical skills, good communication, fits the culture.",
        "gem5_summary": "High-level strategic role requiring technical leadership and business acumen.",
        "gem5_key_challenge": "Scaling the engineering team while maintaining high code quality.",
        "gem1": {"json": {"content": "Sample content from GEM1"}},
        "gem2": {"json": {"content": "Sample content from GEM2"}},
        "gem3": {"json": {"content": "Sample content from GEM3"}},
        "sources_index": "cv_text, interview_notes",
        "tests_text": "Passed all technical tests with flying colors.",
        "case_notes": "Solved the business case efficiently.",
        "references_text": "All references were positive.",
        "client_culture": "Collaborative and fast-paced."
    }

    gems = ["gem1", "gem2", "gem3", "gem4", "gem5"]

    # Warmup
    for gem in gems:
        build_prompt(gem, variables)

    iterations = 100
    start_time = time.perf_counter()
    for _ in range(iterations):
        for gem in gems:
            build_prompt(gem, variables)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time = (total_time / (iterations * len(gems))) * 1000

    print(f"Total time for {iterations * len(gems)} prompt builds: {total_time:.4f}s")
    print(f"Average time per prompt build: {avg_time:.4f}ms")

if __name__ == "__main__":
    benchmark()
