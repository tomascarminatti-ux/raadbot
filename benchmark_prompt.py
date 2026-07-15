import time
import os
import sys
import json

# Add current directory to path so we can import agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

def benchmark_build_prompt():
    variables = {
        "search_id": "SEARCH-2026",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years of experience in Python and AI." * 100,
        "interview_notes": "Great candidate, strong technical skills." * 50,
        "gem5_summary": "Summary of GEM5 results." * 20
    }

    iterations = 1000

    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    start_time = time.time()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time to build prompt: {avg_time*1000:.6f} ms")

def benchmark_pipeline_init():
    iterations = 1000
    gemini = GeminiClient(api_key="mock")

    start_time = time.time()
    for _ in range(iterations):
        p = Pipeline(gemini=gemini, search_id="test", output_dir="runs/test")
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time to init Pipeline: {avg_time*1000:.6f} ms")

if __name__ == "__main__":
    try:
        benchmark_build_prompt()
        benchmark_pipeline_init()
    except Exception as e:
        import traceback
        traceback.print_exc()
