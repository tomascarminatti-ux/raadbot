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
    """Carga un prompt desde el directorio de prompts (con cache)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_maestro() -> str:
    """Carga el prompt maestro."""
    # load_prompt ya tiene @lru_cache, por lo que load_maestro es eficiente.
    return load_prompt("00_prompt_maestro")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el prompt del GEM
    2. Inyecta {{PROMPT_MAESTRO}}
    3. Reemplaza todas las {{variables}}
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (Usando cache)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro (Primer paso para permitir variables dentro del maestro)
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # BOLT OPTIMIZATION: Usar re.sub con un diccionario para evitar múltiples pasadas
    # y .replace() sucesivos. Esto es O(N) en lugar de O(M*N).

    # El patrón busca {{variable}}
    pattern = re.compile(r"\{\{([^\s}]+)\}\}")

    def replace_func(match):
        key = match.group(1)
        # PROMPT_MAESTRO ya fue inyectado, pero si por alguna razón aparece de nuevo
        if key == "PROMPT_MAESTRO":
            return maestro
        if key in variables:
            val = variables[key]
            if isinstance(val, (dict, list)):
                return json.dumps(val, ensure_ascii=False, indent=2)
            return str(val)
        return match.group(0) # Mantiene el placeholder si no se encuentra

    # Inyección de variables en una sola pasada sobre el prompt (que ya incluye el maestro)
    prompt = pattern.sub(replace_func, prompt)

    # Validar que no queden variables sin reemplazar
    remaining = pattern.findall(prompt)
    if remaining:
        # Filtrar VERSION y PROMPT_MAESTRO que se resuelven o son metadata
        remaining = [v for v in remaining if v not in ("VERSION", "PROMPT_MAESTRO")]
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
