import time
import statistics
from agent.prompt_builder import build_prompt

def benchmark_build_prompt():
    variables = {
        "search_id": "TEST-SEARCH",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years of experience in Python and Cloud.",
        "interview_notes": "Great communication skills, strong technical background.",
        "gem5_summary": "Company: TechCorp. Role: Senior Dev. Challenges: Scalability.",
    }

    # Warm up
    for _ in range(5):
        build_prompt("gem1", variables)

    iterations = 100
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        build_prompt("gem1", variables)
        times.append(time.perf_counter() - start)

    avg_time = statistics.mean(times) * 1000  # ms
    print(f"Average build_prompt time: {avg_time:.4f} ms")

if __name__ == "__main__":
    benchmark_build_prompt()
