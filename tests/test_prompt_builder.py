from unittest.mock import patch
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_and_caching():
    """Verifica la carga de prompts y la efectividad del caché LRU con invalidación por mtime."""
    _load_prompt_cached.cache_clear()

    with patch("os.path.getmtime", return_value=100.0):
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

    # Invalidador por mtime simulado
    with patch("os.path.getmtime", return_value=200.0):
        # Carga tras actualización de mtime -> Cache miss (re-lectura)
        load_prompt("gem1")
        info3 = _load_prompt_cached.cache_info()
        assert info3.misses == 2


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
