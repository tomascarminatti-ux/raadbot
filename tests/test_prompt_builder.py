import os
import pytest
import time
from agent.prompt_builder import build_prompt, clear_prompt_caches, get_required_variables

def test_prompt_builder_correctness():
    # Clear caches to start fresh
    clear_prompt_caches()

    # Test variable injection on gem1 (which does not have placeholders by default)
    variables = {
        "candidate_id": "TEST-CANDIDATE",
        "input": {"key": "value"}
    }

    prompt = build_prompt("gem1", variables)

    # Assert gem1-specific text is in prompt
    assert "GEM 1, Agente de Inteligencia de Talento" in prompt
    assert "Google X-Ray" in prompt


def test_prompt_builder_placeholder_replacement():
    # Since prompt_builder's load_prompt loads from prompts directory,
    # let's test that build_prompt replaces placeholders correctly if they exist.
    # We can temporarily mock load_prompt to return a template with placeholders.
    import agent.prompt_builder as pb
    original_load_prompt = pb.load_prompt
    original_load_maestro = pb.load_maestro

    try:
        pb.load_prompt = lambda name: "Hello {{name}}! Welcome to {{company_name}}. Maestro says: {{PROMPT_MAESTRO}}"
        pb.load_maestro = lambda: "Be professional."

        variables = {
            "name": "Jules",
            "company_name": "RAAD"
        }

        # Build prompt using the mocked loader
        prompt = pb.build_prompt("dummy", variables)

        assert "Hello Jules!" in prompt
        assert "Welcome to RAAD." in prompt
        assert "Maestro says: Be professional." in prompt

    finally:
        pb.load_prompt = original_load_prompt
        pb.load_maestro = original_load_maestro


def test_get_required_variables():
    vars_gem1 = get_required_variables("gem1")
    assert isinstance(vars_gem1, list)
    # Ensure standard auto-resolved variables are NOT present
    assert "PROMPT_MAESTRO" not in vars_gem1
    assert "VERSION" not in vars_gem1


def test_benchmark_prompt_builder_performance():
    # Let's benchmark and verify caching benefit
    clear_prompt_caches()

    variables = {
        "candidate_id": "BENCHMARK-CAND",
        "input": {"data": "test"}
    }

    # First run (cache miss, disk I/O)
    start_time = time.perf_counter()
    prompt1 = build_prompt("gem1", variables)
    first_run_duration = time.perf_counter() - start_time

    # Subsequent run (cache hit, fast string operation)
    start_time = time.perf_counter()
    prompt2 = build_prompt("gem1", variables)
    subsequent_run_duration = time.perf_counter() - start_time

    assert prompt1 == prompt2

    print(f"\n⚡ First run duration (Cache Miss): {first_run_duration * 1000:.4f} ms")
    print(f"⚡ Subsequent run duration (Cache Hit): {subsequent_run_duration * 1000:.4f} ms")

    # Typically subsequent runs should be much faster due to cached file reads and precompiled regexes
    assert subsequent_run_duration < 0.01  # < 10ms
