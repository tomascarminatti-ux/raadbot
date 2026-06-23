
import time
import os
import sys
import re
import json

# Add the current directory to sys.path to import agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def build_prompt_legacy(gem_name: str, variables: dict) -> str:
    # Cargar prompt maestro y del GEM (Mocked for legacy)
    from agent.prompt_builder import load_maestro, load_prompt
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Inyectar variables
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        if isinstance(value, dict):
            value = json.dumps(value, ensure_ascii=False, indent=2)
        prompt = prompt.replace(placeholder, str(value))
    return prompt

def verify_correctness():
    print("Verifying correctness...")
    variables = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer.",
        "interview_notes": "Great communication.",
        "gem5_summary": "Summary of GEM5",
        "complex_var": {"a": 1, "b": [1, 2]}
    }

    # Test with gem1
    legacy_output = build_prompt_legacy("gem1", variables)
    optimized_output = build_prompt("gem1", variables)

    # We need to ignore the "Variables sin reemplazar" print if any

    if legacy_output == optimized_output:
        print("✅ Correctness verified: Outputs match exactly.")
    else:
        print("❌ Correctness verification failed: Outputs differ.")
        # Find difference
        for i in range(min(len(legacy_output), len(optimized_output))):
            if legacy_output[i] != optimized_output[i]:
                print(f"First diff at index {i}: legacy='{legacy_output[i-10:i+10]}', opt='{optimized_output[i-10:i+10]}'")
                break
        return False
    return True

def benchmark_build_prompt():
    variables = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software engineer with 10 years of experience in Python and Cloud.",
        "interview_notes": "Great communication skills, strong technical background.",
        "gem5_summary": "Summary of GEM5",
        "gem1": {"key": "value"},
        "gem2": {"key": "value"},
        "gem3": {"key": "value"},
        "sources_index": "cv_text, interview_notes"
    }

    print("Benchmarking optimized build_prompt...")
    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time per optimized build_prompt call: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    if verify_correctness():
        benchmark_build_prompt()
    else:
        sys.exit(1)
