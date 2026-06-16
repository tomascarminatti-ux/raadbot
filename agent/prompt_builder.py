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
    """Carga un prompt desde el directorio de prompts. Cacheado para evitar E/S repetida."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro. Cacheado ya que es estático."""
    return load_prompt("00_prompt_maestro")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM de forma eficiente.

    1. Carga el prompt del GEM (desde cache)
    2. Inyecta {{PROMPT_MAESTRO}} (desde cache)
    3. Reemplaza todas las {{variables}} en un solo pase de regex
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (ambos cacheados)
    maestro = load_maestro()
    template = load_prompt(gem_name)

    # Inyectar prompt maestro primero para expandir sus posibles variables
    template = template.replace("{{PROMPT_MAESTRO}}", maestro)

    # Preparar variables (serializar dicts una sola vez)
    processed_vars = {}
    for k, v in variables.items():
        if isinstance(v, dict):
            processed_vars[k] = json.dumps(v, ensure_ascii=False, indent=2)
        else:
            processed_vars[k] = str(v)

    # Reemplazo de variables en un solo pase usando regex para mayor eficiencia
    # en lugar de múltiples llamadas a .replace() que escanean el string repetidamente.
    def replace_match(match):
        key = match.group(1)
        return processed_vars.get(key, match.group(0))

    prompt = re.sub(r"\{\{(\w+)\}\}", replace_match, template)

    # Validar que no queden variables sin reemplazar
    remaining = re.findall(r"\{\{(\w+)\}\}", prompt)
    if remaining:
        # Filtrar VERSION que es metadata, no un input
        remaining = [v for v in remaining if v != "VERSION"]
        if remaining:
            # Mantener el print original para no romper comportamiento esperado de logueo
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
