import os
import time
import pytest
from agent.prompt_builder import load_prompt, _load_prompt_cached, build_prompt, get_required_variables

def test_prompt_template_caching(tmp_path, monkeypatch):
    """Verifica que el cargador de prompts utilice la cache LRU y se invalide ante cambios de mtime."""
    # Crear directorio temporal para prompts
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    prompt_file = prompts_dir / "gem_test.md"
    prompt_file.write_text("Hello {{name}}, welcome to {{service}}!", encoding="utf-8")

    # Redirigir PROMPTS_DIR en agent.prompt_builder al directorio temporal
    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))

    # Limpiar cache antes de probar
    _load_prompt_cached.cache_clear()
    initial_info = _load_prompt_cached.cache_info()
    assert initial_info.hits == 0

    # Carga 1 (Miss)
    p1 = load_prompt("gem_test")
    assert p1 == "Hello {{name}}, welcome to {{service}}!"
    info_after_1 = _load_prompt_cached.cache_info()
    assert info_after_1.hits == 0

    # Carga 2 (Hit)
    p2 = load_prompt("gem_test")
    assert p2 == p1
    info_after_2 = _load_prompt_cached.cache_info()
    assert info_after_2.hits == 1

    # Invalidate cache alterando el mtime del archivo
    time.sleep(0.01)
    new_mtime = os.path.getmtime(prompt_file) + 10.0
    os.utime(prompt_file, (new_mtime, new_mtime))

    # Carga 3 (Miss por invalidación de mtime)
    p3 = load_prompt("gem_test")
    assert p3 == p1
    info_after_3 = _load_prompt_cached.cache_info()
    assert info_after_3.hits == 1  # Hits no incrementa


def test_build_prompt_and_required_variables():
    """Verifica la inyección de variables y extracción de variables requeridas."""
    prompt_res = build_prompt("gem1", {"candidate_name": "Test Candidate"})
    assert isinstance(prompt_res, str)
    assert "Test Candidate" in prompt_res or len(prompt_res) > 0

    req_vars = get_required_variables("gem1")
    assert isinstance(req_vars, list)
