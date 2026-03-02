import time
import sys
import os

# Add parent directory to path to import agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    """Benchmark the prompt building process."""
    variables = {
        "candidate_id": "CAND-001",
        "search_id": "SEARCH-001",
        "input": {
            "name": "John Doe",
            "experience": "10 years",
            "skills": ["Python", "FastAPI", "React"],
            "education": {
                "degree": "CS",
                "university": "Stanford"
            }
        }
    }

    iterations = 2000

    # Warm up
    for _ in range(100):
        build_prompt("gem1", variables)

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()
    avg = (end_time - start_time) / iterations

    print(f"Average time per build_prompt: {avg*1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
