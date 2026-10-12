import os
import time
import pytest
import agent.prompt_builder as pb
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)

def test_load_prompt_caching(tmp_path):
    """Verifica que _load_prompt_cached use cache LRU e invalide al cambiar mtime."""
    prompt_file = tmp_path / "test_gem.md"
    prompt_file.write_text("Hello {{name}}", encoding="utf-8")

    filepath = str(prompt_file)

    # Limpiar cache inicial
    _load_prompt_cached.cache_clear()

    mtime1 = os.path.getmtime(filepath)
    content1 = _load_prompt_cached(filepath, mtime1)
    assert content1 == "Hello {{name}}"

    info1 = _load_prompt_cached.cache_info()
    assert info1.hits == 0
    assert info1.misses == 1

    # Segunda llamada con el mismo mtime debe ser cache hit
    content2 = _load_prompt_cached(filepath, mtime1)
    assert content2 == "Hello {{name}}"

    info2 = _load_prompt_cached.cache_info()
    assert info2.hits == 1
    assert info2.misses == 1

    # Modificar archivo y actualizar mtime para invalidar cache
    time.sleep(0.01)
    prompt_file.write_text("Updated {{name}}", encoding="utf-8")
    mtime2 = os.path.getmtime(filepath)
    assert mtime2 != mtime1

    content3 = _load_prompt_cached(filepath, mtime2)
    assert content3 == "Updated {{name}}"

    info3 = _load_prompt_cached.cache_info()
    assert info3.misses == 2


def test_build_prompt_variables(tmp_path, monkeypatch):
    """Verifica la inyección correcta de variables y prompt maestro."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "00_prompt_maestro.md").write_text("MAESTRO_HEADER", encoding="utf-8")
    (prompts_dir / "gem_test.md").write_text("{{PROMPT_MAESTRO}}\nHello {{user_name}}, welcome to {{service_name}}!", encoding="utf-8")

    monkeypatch.setattr(pb, "PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    res = pb.build_prompt("gem_test", {"user_name": "Jules", "service_name": "Raadbot"})
    assert "MAESTRO_HEADER" in res
    assert "Hello Jules, welcome to Raadbot!" in res
    assert "{{user_name}}" not in res
    assert "{{service_name}}" not in res


def test_get_required_variables(tmp_path, monkeypatch):
    """Verifica que se extraigan las variables requeridas excluyendo las auto-resueltas."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "00_prompt_maestro.md").write_text("MAESTRO", encoding="utf-8")
    (prompts_dir / "gem_vars.md").write_text("{{PROMPT_MAESTRO}} {{VERSION}} {{candidate_id}} {{job_title}}", encoding="utf-8")

    monkeypatch.setattr(pb, "PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    vars_found = pb.get_required_variables("gem_vars")
    assert set(vars_found) == {"candidate_id", "job_title"}
