"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import json
from functools import lru_cache


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


@lru_cache(maxsize=16)
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
    Construye el prompt final para un GEM (Optimizado).

    1. Carga el prompt del GEM (desde caché si es posible)
    2. Inyecta {{PROMPT_MAESTRO}} (desde caché)
    3. Reemplaza todas las {{variables}} en un solo pase de regex
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (cacheado vía @lru_cache)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro primero (puede contener placeholders propios)
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Preparar mapa de sustitución: serializar dicts a JSON una sola vez
    subs = {}
    for k, v in variables.items():
        if isinstance(v, dict):
            subs[k] = json.dumps(v, ensure_ascii=False, indent=2)
        else:
            subs[k] = str(v)

    # Sustitución en un solo pase usando re.sub con callback
    # El patrón r'\{\{\s*(\w+)\s*\}\}' soporta {{ variable }}
    # con espacios opcionales
    pattern = re.compile(r"\{\{\s*(\w+)\s*\}\}")

    def replace_func(match):
        var_name = match.group(1)
        return subs.get(var_name, match.group(0))

    prompt = pattern.sub(replace_func, prompt)

    # Validar que no queden variables sin reemplazar
    remaining = re.findall(r"\{\{\s*(\w+)\s*\}\}", prompt)
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
    variables = re.findall(r"\{\{\s*(\w+)\s*\}\}", prompt)
    # Filtrar las que se resuelven automáticamente
    auto_resolved = {"PROMPT_MAESTRO", "VERSION"}
    return [v for v in set(variables) if v not in auto_resolved]
