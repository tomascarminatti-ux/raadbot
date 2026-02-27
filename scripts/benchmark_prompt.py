import time
import os
import sys
from functools import lru_cache

# Add root to path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "test-search",
        "candidate_id": "cand-123",
        "context": {"key": "value", "nested": [1, 2, 3]}
    }

    # Warm up (though current code has no cache)
    build_prompt("gem1", variables)

    start = time.perf_counter()
    n = 1000
    for _ in range(n):
        build_prompt("gem1", variables)
    end = time.perf_counter()

    avg_ms = (end - start) * 1000 / n
    print(f"Average build_prompt time: {avg_ms:.4f} ms")

if __name__ == "__main__":
    benchmark()
