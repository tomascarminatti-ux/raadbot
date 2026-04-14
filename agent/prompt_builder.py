"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import functools
import json


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
VARIABLE_PATTERN = re.compile(r"\{\{(\w+)\}\}")


@functools.lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (con cache)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_maestro() -> str:
    """Carga el prompt maestro."""
    return load_prompt("00_prompt_maestro")


@functools.lru_cache(maxsize=32)
def get_base_prompt(gem_name: str) -> str:
    """
    Obtiene el prompt base con el maestro ya inyectado (con cache).
    """
    maestro = load_maestro()
    prompt = load_prompt(gem_name)
    return prompt.replace("{{PROMPT_MAESTRO}}", maestro)


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el prompt base (con maestro ya inyectado)
    2. Reemplaza todas las {{variables}} en una sola pasada usando regex
    3. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Obtener prompt base (maestro ya inyectado y cacheado)
    prompt = get_base_prompt(gem_name)

    # Reemplazar variables en una sola pasada
    def replace_match(match):
        key = match.group(1)
        if key in variables:
            value = variables[key]
            if isinstance(value, dict):
                return json.dumps(value, ensure_ascii=False, indent=2)
            return str(value)
        return match.group(0)  # Mantener placeholder si no hay valor

    prompt = VARIABLE_PATTERN.sub(replace_match, prompt)

    # Validar que no queden variables sin reemplazar
    remaining = VARIABLE_PATTERN.findall(prompt)
    if remaining:
        # Filtrar VERSION que es metadata, no un input
        remaining = [v for v in remaining if v != "VERSION"]
        if remaining:
            print(f"  ⚠️  Variables sin reemplazar: {remaining}")

    return prompt


def get_required_variables(gem_name: str) -> list[str]:
    """
    Extrae las variables requeridas de un prompt.

    Returns:
        Lista de nombres de variables (sin {{ }})
    """
    prompt = load_prompt(gem_name)
    variables = VARIABLE_PATTERN.findall(prompt)
    # Filtrar las que se resuelven automáticamente
    auto_resolved = {"PROMPT_MAESTRO", "VERSION"}
    return [v for v in set(variables) if v not in auto_resolved]
