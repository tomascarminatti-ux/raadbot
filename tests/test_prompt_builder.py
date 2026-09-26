import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached
)

def test_load_prompt_caching(tmp_path, monkeypatch):
    """Verifica que load_prompt utilice el cache LRU y se invalide si cambia el mtime."""
    # Crear un directorio temporal de prompts y apuntar PROMPTS_DIR a él
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    test_gem = prompts_dir / "gem_test.md"
    test_gem.write_text("Hello {{name}}!", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))

    # Limpiar el cache antes del test
    _load_prompt_cached.cache_clear()

    # Primer llamado: Miss
    content1 = load_prompt("gem_test")
    assert content1 == "Hello {{name}}!"
    info1 = _load_prompt_cached.cache_info()
    assert info1.hits == 0
    assert info1.misses == 1

    # Segundo llamado: Hit
    content2 = load_prompt("gem_test")
    assert content2 == "Hello {{name}}!"
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits == 1

    # Modificar el archivo (cambiando mtime)
    new_mtime = os.path.getmtime(str(test_gem)) + 10.0
    test_gem.write_text("Updated {{name}}!", encoding="utf-8")
    os.utime(str(test_gem), (new_mtime, new_mtime))

    # Tercer llamado tras actualización de mtime: Miss (cache invalidated)
    content3 = load_prompt("gem_test")
    assert content3 == "Updated {{name}}!"
    info3 = _load_prompt_cached.cache_info()
    assert info3.misses == 2


def test_build_prompt_variables(tmp_path, monkeypatch):
    """Verifica que build_prompt resuelva correctamente el prompt maestro y variables."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    maestro_file = prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("MAESTRO PROMPT", encoding="utf-8")

    gem_file = prompts_dir / "gem1.md"
    gem_file.write_text("Header: {{PROMPT_MAESTRO}}\nUser: {{user_name}}", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    res = build_prompt("gem1", {"user_name": "Alice"})
    assert "Header: MAESTRO PROMPT" in res
    assert "User: Alice" in res


def test_get_required_variables(tmp_path, monkeypatch):
    """Verifica la extracción de variables requeridas omitiendo PROMPT_MAESTRO y VERSION."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    gem_file = prompts_dir / "gem2.md"
    gem_file.write_text("{{PROMPT_MAESTRO}} {{VERSION}} {{var1}} {{var2}}", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    req = get_required_variables("gem2")
    assert set(req) == {"var1", "var2"}
