"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import json
import functools


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


@functools.lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (Cacheado)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@functools.lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro (Cacheado)."""
    return load_prompt("00_prompt_maestro")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM de forma eficiente.

    1. Carga el prompt del GEM y el maestro (desde cache)
    2. Realiza el reemplazo de variables en un solo paso de regex
    3. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Preparar el mapa de reemplazo (convertir dicts a JSON string una sola vez)
    # También incluimos la versión si está en las variables, sino se ignora en la validación
    replace_map = {}
    for k, v in variables.items():
        if isinstance(v, dict):
            replace_map[k] = json.dumps(v, ensure_ascii=False, indent=2)
        else:
            replace_map[k] = str(v)

    # Reemplazo en un solo paso usando regex para mayor velocidad
    pattern = re.compile(r"\{\{(\w+)\}\}")

    def replacer(match):
        key = match.group(1)
        return replace_map.get(key, match.group(0))

    prompt = pattern.sub(replacer, prompt)

    # Validar que no queden variables sin reemplazar
    remaining = pattern.findall(prompt)
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
