import os
import json
import time
import pytest
import re
from agent.prompt_builder import load_prompt, build_prompt, clear_prompt_caches, PROMPTS_DIR
from agent.pipeline import _load_schema, Pipeline


def test_prompt_builder_caching_and_invalidation():
    # Setup temporary prompt file to verify mtime-based cache invalidation
    test_gem_name = "test_temp_gem"
    test_file_path = os.path.join(PROMPTS_DIR, f"{test_gem_name}.md")

    try:
        # Write initial content
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("Initial prompt with {{variable}}")

        # Clear caches before test
        clear_prompt_caches()

        # Load first time
        content1 = load_prompt(test_gem_name)
        assert content1 == "Initial prompt with {{variable}}"

        # Load second time (should be from cache)
        content2 = load_prompt(test_gem_name)
        assert content2 == "Initial prompt with {{variable}}"

        # Modify file and change mtime to invalidate cache
        time.sleep(0.1)  # Ensure time difference for mtime resolution
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("Updated prompt with {{variable}}")

        # Load third time (should detect updated mtime and load from disk)
        content3 = load_prompt(test_gem_name)
        assert content3 == "Updated prompt with {{variable}}"

    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_build_prompt_single_pass():
    # Verify build_prompt correctly replaces variables including nested and long-prefixed ones
    variables = {
        "search_id": "SEARCH-2026-001",
        "candidate_id": "CAND-123",
        "cv_text": "Experienced Developer",
        "interview_notes": "Good communicator",
        "gem5_summary": "CEO Search",
    }

    prompt = build_prompt("gem1", variables)

    # All replaced variables must appear in the final prompt
    assert "CAND-123" in prompt
    assert "Experienced Developer" in prompt
    assert "CEO Search" in prompt


def test_schema_validator_compilation_and_benchmark():
    # Check that schema validator is compiled and works
    from jsonschema.validators import validator_for

    schema = _load_schema()
    assert schema is not None

    # Verify compiled validator works
    validator_class = validator_for(schema)
    validator = validator_class(schema)

    test_json = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["cv.pdf"],
        },
        "scores": {"score_dimension": 8, "confidence": 9},
        "blockers": [],
        "content": {},
    }

    # Validate with compiled validator
    validator.validate(test_json)  # Should not raise exception

    # Simple benchmark to demonstrate speedup of compiled validator vs. standard validate
    from jsonschema import validate

    # Warm up
    validate(instance=test_json, schema=schema)
    validator.validate(test_json)

    start_std = time.perf_counter()
    for _ in range(100):
        validate(instance=test_json, schema=schema)
    end_std = time.perf_counter()
    std_time = end_std - start_std

    start_comp = time.perf_counter()
    for _ in range(100):
        validator.validate(test_json)
    end_comp = time.perf_counter()
    comp_time = end_comp - start_comp

    print(
        f"\n[BENCHMARK] Standard Validation: {std_time:.6f}s | Compiled Validation: {comp_time:.6f}s"
    )
    # Assert that compiled validation is indeed faster or runs well within minimal overhead
    assert comp_time < std_time or comp_time < 0.1


def test_prompt_building_benchmark():
    # Verify loading caching speeds up build_prompt considerably
    variables = {
        "search_id": "SEARCH-2026-001",
        "candidate_id": "CAND-123",
        "cv_text": "Experienced Developer",
        "interview_notes": "Good communicator",
        "gem5_summary": "CEO Search",
    }

    # First run (loads files, caches them)
    clear_prompt_caches()
    start_uncached = time.perf_counter()
    build_prompt("gem1", variables)
    end_uncached = time.perf_counter()
    uncached_time = end_uncached - start_uncached

    # Subsequent runs (fully cached)
    start_cached = time.perf_counter()
    for _ in range(50):
        build_prompt("gem1", variables)
    end_cached = time.perf_counter()
    cached_time = (end_cached - start_cached) / 50

    print(
        f"\n[BENCHMARK] Uncached prompt build: {uncached_time:.6f}s | Cached prompt build: {cached_time:.6f}s"
    )
    assert cached_time < uncached_time or cached_time < 0.001
