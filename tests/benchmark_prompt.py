import time
from agent.prompt_builder import build_prompt, _load_prompt_cached


def benchmark():
    vars_dict = {
        "search_id": "BENCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years in python",
        "interview_notes": "Great communications skills and solid system design",
        "gem5_summary": "High growth scale-up looking for tech lead",
    }

    # Clear cache first
    _load_prompt_cached.cache_clear()

    # Warmup / single execution
    build_prompt("gem1", vars_dict)

    iterations = 5000
    start = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", vars_dict)
    elapsed = time.perf_counter() - start

    avg_us = (elapsed / iterations) * 1_000_000
    print(f"Executed {iterations} iterations in {elapsed:.4f}s ({avg_us:.2f} µs/op)")


if __name__ == "__main__":
    benchmark()
