import time
import os
import sys

# Add current directory to path so we can import agent and utils
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt, load_prompt, load_maestro
from utils.gem_core import validate_contract

def benchmark_prompt_builder(iterations=1000):
    variables = {
        "search_id": "test-search",
        "candidate_id": "test-candidate",
        "context": {
            "search_inputs": {"key": "value" * 10},
            "candidate_data": {"name": "John Doe", "resume": "Expert " * 100},
            "working_memory": [{"step": 1, "agent": "gem1", "observation": "data"}]
        }
    }

    start_time = time.perf_counter()
    for _ in range(iterations):
        # We use gem6 as it's likely complex
        build_prompt("gem6", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average build_prompt time: {avg_time*1000:.4f} ms")

def benchmark_validate_contract(iterations=1000):
    # Create a temporary schema and data
    schema = {
        "score": "number",
        "reason": "string",
        "items": "array",
        "metadata": "object",
        "active": "boolean"
    }
    data = {
        "score": 0.95,
        "reason": "Passed with flying colors",
        "items": [1, 2, 3],
        "metadata": {"source": "test"},
        "active": True
    }

    schema_path = "test_schema.json"
    import json
    with open(schema_path, "w") as f:
        json.dump(schema, f)

    start_time = time.perf_counter()
    for _ in range(iterations):
        validate_contract(data, schema_path)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average validate_contract time: {avg_time*1000:.4f} ms")

    os.remove(schema_path)

if __name__ == "__main__":
    print("Benchmarking performance...")
    benchmark_prompt_builder()
    benchmark_validate_contract()
