import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_and_caching():
    """Verifica la carga de prompts y la efectividad del caché LRU con invalidación por mtime."""
    _load_prompt_cached.cache_clear()

    # Primera carga -> Cache miss
    content1 = load_prompt("gem1")
    info1 = _load_prompt_cached.cache_info()
    assert info1.hits == 0
    assert info1.misses == 1

    # Segunda carga -> Cache hit
    content2 = load_prompt("gem1")
    info2 = _load_prompt_cached.cache_info()
    assert content1 == content2
    assert info2.hits == 1

    # Invalidador por mtime
    filepath = os.path.join(os.path.dirname(__file__), "..", "prompts", "gem1.md")
    current_mtime = os.path.getmtime(filepath)
    # Forzar actualización de mtime
    os.utime(filepath, (current_mtime + 2, current_mtime + 2))

    # Carga tras actualización de mtime -> Cache miss (re-lectura)
    load_prompt("gem1")
    info3 = _load_prompt_cached.cache_info()
    assert info3.misses == 2

    # Restaurar mtime original
    os.utime(filepath, (current_mtime, current_mtime))


def test_build_prompt_variables():
    """Verifica la correcta inyección de variables en templates."""
    required_vars = get_required_variables("gem1")
    vars_dict = {v: f"mock_{v}" for v in required_vars}
    result = build_prompt("gem1", vars_dict)
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_required_variables():
    """Verifica que extrae variables del prompt filtrando las automáticas."""
    vars_found = get_required_variables("gem1")
    assert isinstance(vars_found, list)
    assert "PROMPT_MAESTRO" not in vars_found
    assert "VERSION" not in vars_found
