import os
import json
import time
import tempfile
import functools
import pytest
from jsonschema.validators import validator_for
from agent.prompt_builder import load_prompt, _load_prompt_cached
from agent.pipeline import get_validator

def test_prompt_cache_correctness():
    # Test that prompt caching returns the correct content and invalidates on mtime change
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write("Initial prompt version 1")
        filepath = tmp.name

    try:
        # Check initial load
        mtime = os.path.getmtime(filepath)
        content1 = _load_prompt_cached(filepath, mtime)
        assert content1 == "Initial prompt version 1"

        # Check cached load (mtime hasn't changed)
        content2 = _load_prompt_cached(filepath, mtime)
        assert content2 == "Initial prompt version 1"

        # Write new content and update mtime
        time.sleep(0.01) # Ensure file time changes
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("Updated prompt version 2")

        # New mtime
        new_mtime = os.path.getmtime(filepath)
        assert new_mtime != mtime

        # Check cached load with new mtime
        content3 = _load_prompt_cached(filepath, new_mtime)
        assert content3 == "Updated prompt version 2"

    finally:
        os.remove(filepath)


def test_schema_validator_compilation():
    # Verify that the get_validator function successfully loads and compiles the schema
    validator = get_validator()
    assert validator is not None
    assert hasattr(validator, "validate")
    assert validator.schema is not None
    assert "$schema" in validator.schema
