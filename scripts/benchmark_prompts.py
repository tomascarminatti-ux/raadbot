
import time
import os
import sys

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "test-search",
        "candidate_id": "test-candidate",
        "cv_text": "This is a long CV text " * 100,
        "interview_notes": "These are some interview notes " * 50,
        "gem5_summary": "Summary of GEM5 " * 20,
        "gem1": {"some": "json", "data": "here" * 10},
        "tests_text": "Test results " * 30,
        "case_notes": "Case notes " * 30,
        "gem5_key_challenge": "The key challenge is..." * 10,
        "gem2": {"more": "json", "data": "there" * 10},
        "references_text": "References..." * 20,
        "client_culture": "Culture..." * 20,
        "sources_index": "cv, interview, tests",
        "gem3": {"final": "verdict", "score": 8}
    }

    # Try to find a gem that uses many of these
    gem_name = "gem4" # Usually uses gem1, gem2, gem3

    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        build_prompt(gem_name, variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt ('{gem_name}'): {avg_time*1000:.4f} ms")
    print(f"Total time for {iterations} iterations: {end_time - start_time:.4f} s")

if __name__ == "__main__":
    try:
        benchmark()
    except Exception as e:
        print(f"Error during benchmark: {e}")
