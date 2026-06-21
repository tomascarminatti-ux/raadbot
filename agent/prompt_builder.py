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
    Construye el prompt final para un GEM (Optimizado).

    1. Carga el prompt del GEM (via cache)
    2. Inyecta {{PROMPT_MAESTRO}}
    3. Reemplaza todas las {{variables}} en un solo pase de Regex
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (Usando lru_cache para evitar I/O repetitivo)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro primero para permitir variables dentro del maestro
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Pre-procesar variables: convertir dicts a JSON string una sola vez
    processed_vars = {}
    for k, v in variables.items():
        if isinstance(v, dict):
            processed_vars[k] = json.dumps(v, ensure_ascii=False, indent=2)
        else:
            processed_vars[k] = str(v)

    # Reemplazo en un solo pase usando Regex y callback (Más eficiente que múltiples .replace())
    def _replacer(match):
        var_name = match.group(1)
        return processed_vars.get(var_name, match.group(0))

    prompt = re.sub(r"\{\{(\w+)\}\}", _replacer, prompt)

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


def clear_prompt_cache():
    """Limpia la cache de prompts (útil para tests o si se editan archivos en caliente)."""
    load_prompt.cache_clear()
    load_maestro.cache_clear()
