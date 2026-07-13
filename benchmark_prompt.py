import time
import os
import sys

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

variables = {
    "search_id": "test-search",
    "candidate_id": "test-candidate",
    "context": {
        "search_inputs": {"jd": "Software Engineer"},
        "candidate_data": {"cv": "Experienced Python Developer"},
        "working_memory": []
    }
}

# Warmup
try:
    build_prompt("gem6", variables)
except Exception as e:
    print(f"Error during warmup: {e}")
    sys.exit(1)

start = time.perf_counter()
iterations = 100
for _ in range(iterations):
    build_prompt("gem6", variables)
end = time.perf_counter()

print(f"Time for {iterations} builds: {end - start:.4f}s")
print(f"Average time: {(end - start)/iterations:.6f}s")
