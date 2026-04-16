"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import json
from functools import lru_cache


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


@lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (Cacheado)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro (Cacheado)."""
    return load_prompt("00_prompt_maestro")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el prompt del GEM
    2. Inyecta {{PROMPT_MAESTRO}} (soporta placeholders dentro del maestro)
    3. Reemplaza todas las {{variables}}
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar maestro primero (para que sus variables se procesen después)
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    def _replace_match(match):
        key = match.group(1)
        if key in variables:
            val = variables[key]
            if isinstance(val, dict):
                return json.dumps(val, ensure_ascii=False, indent=2)
            return str(val)
        return match.group(0)

    # Reemplazo en un solo paso usando regex (incluye guiones y puntos en llaves)
    prompt = re.sub(r"\{\{([a-zA-Z0-9_.-]+)\}\}", _replace_match, prompt)

    # Validar que no queden variables sin reemplazar
    remaining = re.findall(r"\{\{(\w+)\}\}", prompt)
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
    variables = re.findall(r"\{\{(\w+)\}\}", prompt)
    # Filtrar las que se resuelven automáticamente
    auto_resolved = {"PROMPT_MAESTRO", "VERSION"}
    return [v for v in set(variables) if v not in auto_resolved]
