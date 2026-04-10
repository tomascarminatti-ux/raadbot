import time
import os
import sys
import json

sys.path.append(os.getcwd())
from utils.gem_core import validate_contract

def benchmark():
    contract = {"score": "number", "items": "array"}
    os.makedirs("contracts", exist_ok=True)
    with open("contracts/test_output.schema.json", "w") as f:
        json.dump(contract, f)

    data = {"score": 0.8, "items": [1, 2, 3]}
    path = "contracts/test_output.schema.json"

    # Pre-warm
    validate_contract(data, path)

    start = time.perf_counter()
    n = 1000
    for _ in range(n):
        validate_contract(data, path)
    end = time.perf_counter()

    avg_time = (end - start) / n * 1000
    print(f"Average validate_contract time: {avg_time:.4f} ms")

if __name__ == "__main__":
    benchmark()
