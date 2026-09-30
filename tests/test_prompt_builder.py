import os
import time
from agent.prompt_builder import load_prompt, build_prompt, build_agent_prompt, get_required_variables, _load_prompt_cached


def test_load_prompt_caching():
    """Verifica que load_prompt utiliza la caché y responde correctamente."""
    prompt1 = load_prompt("gem1")
    cache_info1 = _load_prompt_cached.cache_info()

    prompt2 = load_prompt("gem1")
    cache_info2 = _load_prompt_cached.cache_info()

    assert prompt1 == prompt2
    assert cache_info2.hits > cache_info1.hits


def test_build_agent_prompt_payload_injection():
    """Verifica que build_agent_prompt inyecta el payload correctamente."""
    built = build_agent_prompt("gem5", {"test_key": "test_input_value"})
    assert "test_input_value" in built


def test_get_required_variables_returns_list():
    """Verifica la extracción de variables requeridas."""
    vars_list = get_required_variables("gem5")
    assert isinstance(vars_list, list)
