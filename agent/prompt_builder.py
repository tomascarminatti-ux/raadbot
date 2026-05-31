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


@functools.lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro (con cache)."""
    return load_prompt("00_prompt_maestro")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el prompt del GEM
    2. Inyecta {{PROMPT_MAESTRO}}
    3. Reemplaza todas las {{variables}} usando single-pass regex
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (cacheado)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro explícitamente para permitir que contenga sus propios placeholders
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Reemplazo en una sola pasada usando regex y callback
    def replace_match(match):
        key = match.group(1)
        if key in variables:
            val = variables[key]
            if isinstance(val, (dict, list)):
                return json.dumps(val, ensure_ascii=False, indent=2)
            return str(val)
        return match.group(0)  # Mantener placeholder si no hay variable

    prompt = VARIABLE_PATTERN.sub(replace_match, prompt)

    # Validar variables restantes (excepto VERSION)
    remaining = VARIABLE_PATTERN.findall(prompt)
    remaining = [v for v in remaining if v != "VERSION"]
    if remaining:
        # Usamos logger si estuviera disponible, pero mantenemos print para paridad con original
        print(f"  ⚠️  Variables sin reemplazar en {gem_name}: {remaining}")

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


def clear_caches():
    """Limpia los caches de prompts (útil para tests o recarga en caliente)."""
    load_prompt.cache_clear()
    load_maestro.cache_clear()
