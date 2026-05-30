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
    """Carga un prompt desde el directorio de prompts."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@functools.lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro."""
    return load_prompt("00_prompt_maestro")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el prompt del GEM
    2. Inyecta {{PROMPT_MAESTRO}} (vía el callback de reemplazo)
    3. Reemplaza todas las {{variables}} en un solo pase
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt del GEM
    prompt = load_prompt(gem_name)

    # Inyectar PROMPT_MAESTRO primero para permitir que contenga sus propias variables
    # Este es el único reemplazo "especial" que ocurre antes del pase general
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", load_maestro())

    # Preparar el pool de variables
    # Se usa un diccionario para acceso O(1) durante el reemplazo
    all_vars = variables.copy()

    # Callback para re.sub que maneja la lógica de reemplazo
    def replace_var(match):
        key = match.group(1)
        if key in all_vars:
            val = all_vars[key]
            if isinstance(val, dict):
                return json.dumps(val, ensure_ascii=False, indent=2)
            return str(val)
        # Si no existe en all_vars, se mantiene el placeholder original
        return match.group(0)

    # Reemplazo en un solo pase usando el regex pre-compilado
    prompt = VARIABLE_PATTERN.sub(replace_var, prompt)

    # Validar que no queden variables sin reemplazar (excluyendo VERSION)
    remaining = VARIABLE_PATTERN.findall(prompt)
    if remaining:
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
