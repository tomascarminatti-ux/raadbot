import time
import os
import sys

# Asegurar que el directorio raíz esté en el path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "TEST-123",
        "candidate_id": "CAND-456",
        "context": {
            "name": "John Doe",
            "experience": "10 years",
            "skills": ["Python", "AI", "Performance"],
            "education": "PhD in Computer Science"
        }
    }

    # Warm up
    for _ in range(5):
        build_prompt("gem1", variables)

    start_time = time.time()
    iterations = 100
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_latency = (end_time - start_time) / iterations * 1000
    print(f"Average latency for build_prompt (100 iterations): {avg_latency:.4f} ms")

if __name__ == "__main__":
    benchmark()
