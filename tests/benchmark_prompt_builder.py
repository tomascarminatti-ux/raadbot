import time
from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "SEARCH-123",
        "candidate_id": "CAND-456",
        "cv_text": "Experienced software engineer with strong Python background.",
        "interview_notes": "Great technical skills, communication is clear.",
        "gem5_summary": "Company needs a senior backend engineer to scale systems.",
        "gem1": '{"scores": {"score_dimension": 8}}',
        "gem2": '{"scores": {"score_dimension": 7}}',
        "gem3": '{"scores": {"score_dimension": 7}}',
        "sources_index": "cv_text, interview_notes",
    }

    # Warm up
    build_prompt("gem1", variables)

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
        build_prompt("gem2", variables)
        build_prompt("gem3", variables)
        build_prompt("gem4", variables)
        build_prompt("gem5", variables)
    end_time = time.perf_counter()

    elapsed = end_time - start_time
    print(f"Time for {iterations * 5} prompt builds: {elapsed:.4f} seconds")
    print(f"Average time per build: {(elapsed / (iterations * 5)) * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
