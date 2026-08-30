import os
import pytest
from agent.prompt_builder import load_prompt, build_prompt, clear_prompt_caches, get_required_variables


def test_load_prompt_caching(tmp_path, monkeypatch):
    """Verifica que load_prompt devuelva valores cacheados y que clear_prompt_caches los invalide."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    maestro_file = prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("PROMPT MAESTRO BASE", encoding="utf-8")

    gem_file = prompts_dir / "gem_test.md"
    gem_file.write_text("Prompt test {{name}} {{PROMPT_MAESTRO}}", encoding="utf-8")

    import agent.prompt_builder as pb
    monkeypatch.setattr(pb, "PROMPTS_DIR", str(prompts_dir))

    clear_prompt_caches()

    # Primera llamada - lee de disco
    c1 = load_prompt("gem_test")
    assert c1 == "Prompt test {{name}} {{PROMPT_MAESTRO}}"

    # Modificar archivo en disco sin limpiar la caché
    gem_file.write_text("Prompt MODIFICADO {{name}}", encoding="utf-8")

    # Segunda llamada - debe retornar el valor cacheado previo
    c2 = load_prompt("gem_test")
    assert c2 == "Prompt test {{name}} {{PROMPT_MAESTRO}}"

    # Limpiar caché e invocar de nuevo - debe retornar el contenido actualizado
    clear_prompt_caches()
    c3 = load_prompt("gem_test")
    assert c3 == "Prompt MODIFICADO {{name}}"


def test_build_prompt_with_cache(tmp_path, monkeypatch):
    """Verifica la construcción correcta de prompts utilizando el layer de caché e inyección de variables."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    (prompts_dir / "00_prompt_maestro.md").write_text("MAESTRO_CONTENT", encoding="utf-8")
    (prompts_dir / "gem_test.md").write_text("HEADER: {{PROMPT_MAESTRO}} | Val: {{val}}", encoding="utf-8")

    import agent.prompt_builder as pb
    monkeypatch.setattr(pb, "PROMPTS_DIR", str(prompts_dir))

    clear_prompt_caches()

    res = build_prompt("gem_test", {"val": "123"})
    assert res == "HEADER: MAESTRO_CONTENT | Val: 123"

    req_vars = get_required_variables("gem_test")
    assert req_vars == ["val"]
