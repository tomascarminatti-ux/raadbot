import time
import os
import sys

# Add current directory to path to import agent
sys.path.append(os.getcwd())

from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

def benchmark_pipeline_init():
    gemini = GeminiClient(api_key="dummy")

    start_time = time.perf_counter()
    iterations = 100
    for i in range(iterations):
        Pipeline(gemini=gemini, search_id=f"test-{i}", output_dir=f"runs/test-{i}/outputs")
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for Pipeline initialization: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark_pipeline_init()
