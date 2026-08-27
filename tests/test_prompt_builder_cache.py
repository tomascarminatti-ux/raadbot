import os
import tempfile
import pytest
from agent.prompt_builder import load_prompt, clear_prompt_caches, PROMPTS_DIR


def test_prompt_builder_lru_cache():
    """Verifica el comportamiento de la caché LRU al cargar prompts."""
    clear_prompt_caches()

    # Primera llamada: lectura y guardado en caché
    content1 = load_prompt("gem5")
    info1 = load_prompt.cache_info()
    assert info1.hits == 0
    assert info1.misses >= 1

    # Segunda llamada: hit en caché
    content2 = load_prompt("gem5")
    info2 = load_prompt.cache_info()
    assert content1 == content2
    assert info2.hits == info1.hits + 1


def test_prompt_builder_cache_clear():
    """Verifica la invalidación de la caché mediante clear_prompt_caches()."""
    clear_prompt_caches()
    load_prompt("gem5")
    assert load_prompt.cache_info().hits == 0

    load_prompt("gem5")
    assert load_prompt.cache_info().hits == 1

    clear_prompt_caches()
    assert load_prompt.cache_info().hits == 0
    assert load_prompt.cache_info().misses == 0
