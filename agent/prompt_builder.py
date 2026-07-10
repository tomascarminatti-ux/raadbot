"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import functools
import json


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


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


VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM usando reemplazo eficiente de un solo paso.

    1. Carga el prompt del GEM
    2. Inyecta {{PROMPT_MAESTRO}}
    3. Reemplaza todas las {{variables}} en un solo paso regex
    4. Advierte si quedan variables sin reemplazar (excepto {{VERSION}})

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro primero para permitir variables anidadas dentro de él
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Convertir dicts a JSON string por adelantado para optimizar el bucle de reemplazo
    processed_vars = {}
    for key, value in variables.items():
        if isinstance(value, dict):
            processed_vars[key] = json.dumps(value, ensure_ascii=False, indent=2)
        else:
            processed_vars[key] = str(value)

    def replace_func(match):
        var_name = match.group(1)
        if var_name == "VERSION":
            return match.group(0)  # Mantener {{VERSION}} intacto

        replacement = processed_vars.get(var_name)
        if replacement is not None:
            return replacement

        # Si no existe, lo dejamos igual y luego build_prompt avisará
        return match.group(0)

    # Reemplazo de todas las variables en un solo paso eficiente
    final_prompt = VAR_PATTERN.sub(replace_func, prompt)

    # Validar si quedaron variables (excepto VERSION)
    remaining = VAR_PATTERN.findall(final_prompt)
    remaining = [v for v in remaining if v != "VERSION"]
    if remaining:
        print(f"  ⚠️  Variables sin reemplazar en {gem_name}: {remaining}")

    return final_prompt


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
