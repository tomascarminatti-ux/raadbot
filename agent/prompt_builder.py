"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import functools
import json


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


@functools.lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (con caché)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@functools.lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro (con caché)."""
    return load_prompt("00_prompt_maestro")


@functools.lru_cache(maxsize=32)
def _get_template_with_maestro(gem_name: str) -> str:
    """Obtiene el template del GEM con el maestro ya inyectado (con caché)."""
    maestro = load_maestro()
    prompt = load_prompt(gem_name)
    return prompt.replace("{{PROMPT_MAESTRO}}", maestro)


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM optimizado.

    1. Obtiene template (con maestro inyectado y cacheado)
    2. Reemplaza todas las {{variables}} en un solo pase de regex.
    3. Valida que no queden variables críticas sin reemplazar.
    """
    template = _get_template_with_maestro(gem_name)
    missing = []

    def _replace_match(match):
        key = match.group(1)
        if key in variables:
            val = variables[key]
            if isinstance(val, dict):
                return json.dumps(val, ensure_ascii=False, indent=2)
            return str(val)

        # Ignorar VERSION que es metadata interna
        if key != "VERSION":
            missing.append(key)
        return match.group(0)

    # Inyección en un solo pase
    final_prompt = VAR_PATTERN.sub(_replace_match, template)

    if missing:
        # Se mantiene el log original para debugging
        print(f"  ⚠️  Variables sin reemplazar en {gem_name}: {list(set(missing))}")

    return final_prompt


def get_required_variables(gem_name: str) -> list[str]:
    """
    Extrae las variables requeridas de un prompt.

    Returns:
        Lista de nombres de variables (sin {{ }})
    """
    prompt = load_prompt(gem_name)
    variables = VAR_PATTERN.findall(prompt)
    # Filtrar las que se resuelven automáticamente
    auto_resolved = {"PROMPT_MAESTRO", "VERSION"}
    return [v for v in set(variables) if v not in auto_resolved]
