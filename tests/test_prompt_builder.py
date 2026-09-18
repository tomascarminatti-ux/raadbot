import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
    build_agent_prompt,
)

def test_load_prompt_and_caching():
    """Verifica la carga de prompts y la funcionalidad de LRU cache con invalidación por mtime."""
    prompt_1 = load_prompt("gem1")
    assert isinstance(prompt_1, str)
    assert len(prompt_1) > 0

    # Cache info initial check
    info_before = _load_prompt_cached.cache_info()
    assert info_before.hits >= 0

    # Repeat call should hit LRU cache
    prompt_2 = load_prompt("gem1")
    assert prompt_1 == prompt_2
    info_after = _load_prompt_cached.cache_info()
    assert info_after.hits > info_before.hits


def test_cache_invalidation_on_mtime_change(tmp_path):
    """Verifica que modificar la mtime del archivo invalida el cache."""
    prompt_file = tmp_path / "test_prompt.md"
    prompt_file.write_text("Hello {{name}}!", encoding="utf-8")

    filepath = str(prompt_file)
    mtime_1 = os.path.getmtime(filepath)

    res_1 = _load_prompt_cached(filepath, mtime_1)
    assert res_1 == "Hello {{name}}!"

    # Simulate file modification
    prompt_file.write_text("Hello updated {{name}}!", encoding="utf-8")
    new_mtime = mtime_1 + 10.0
    os.utime(filepath, (new_mtime, new_mtime))

    mtime_2 = os.path.getmtime(filepath)
    res_2 = _load_prompt_cached(filepath, mtime_2)
    assert res_2 == "Hello updated {{name}}!"


def test_build_agent_prompt():
    """Verifica la inyección de variables y anexado de payload."""
    result = build_agent_prompt("gem1", {"candidate_name": "Alice"})
    assert isinstance(result, str)
    assert "Alice" in result


def test_get_required_variables():
    """Verifica la extracción de variables requeridas desde el prompt."""
    reqs = get_required_variables("gem1")
    assert isinstance(reqs, list)
    assert "PROMPT_MAESTRO" not in reqs
    assert "VERSION" not in reqs
