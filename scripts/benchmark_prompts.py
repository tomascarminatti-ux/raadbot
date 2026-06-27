
import time
import sys
import os

# Add the root directory to sys.path to import agent modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=1000):
    variables = {
        "search_id": "TEST-SEARCH",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years of experience in Python and Cloud.",
        "interview_notes": "Strong technical skills, good communication.",
        "gem5_summary": "Role requires high scalability expertise.",
        "jd_text": "Senior Backend Engineer role at a fast-growing startup.",
        "kickoff_notes": "Focus on system design and mentorship.",
        "company_context": "Tech industry, Series B startup.",
        "client_culture": "Fast-paced, innovative.",
        "tests_text": "Passed all technical tests with flying colors.",
        "case_notes": "Excellent problem-solving approach.",
        "references_text": "Highly recommended by former colleagues.",
        "sources_index": "cv_text, interview_notes, tests_text"
    }

    gem_names = ["gem1", "gem2", "gem3", "gem4", "gem5"]

    start_time = time.time()
    for _ in range(iterations):
        for gem_name in gem_names:
            try:
                build_prompt(gem_name, variables)
            except Exception:
                pass # Some gems might not exist or have different requirements
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Total time for {iterations * len(gem_names)} prompt builds: {total_time:.4f} seconds")
    print(f"Average time per prompt build: {(total_time / (iterations * len(gem_names))) * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark_build_prompt()
