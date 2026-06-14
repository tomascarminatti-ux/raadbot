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
    """Carga un prompt desde el directorio de prompts (con caché)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro (con caché)."""
    return load_prompt("00_prompt_maestro")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el prompt del GEM
    2. Inyecta {{PROMPT_MAESTRO}}
    3. Reemplaza todas las {{variables}} en un solo paso
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (desde caché si es posible)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro primero para que también pueda contener variables
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Preparar el diccionario de reemplazo (JSON strings para dicts)
    replace_dict = {}
    for k, v in variables.items():
        if isinstance(v, dict):
            replace_dict[k] = json.dumps(v, ensure_ascii=False, indent=2)
        else:
            replace_dict[k] = str(v)

    # Reemplazo de variables en un solo paso usando regex
    pattern = re.compile(r"\{\{(\w+)\}\}")

    def replace_match(match):
        key = match.group(1)
        return replace_dict.get(key, match.group(0))

    prompt = pattern.sub(replace_match, prompt)

    # Validar que no queden variables sin reemplazar (excepto VERSION)
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
