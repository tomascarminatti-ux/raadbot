import time
import os
import sys

# Add current dir to path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

variables = {
    "search_id": "TEST-123",
    "candidate_id": "CAND-456",
    "context": {"some": "data", "more": "data"}
}

start = time.time()
for _ in range(1000):
    build_prompt("gem1", variables)
end = time.time()

print(f"Time for 1000 build_prompt calls: {end - start:.4f}s")
