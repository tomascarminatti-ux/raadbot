"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import json
from functools import lru_cache


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
VARIABLE_PATTERN = re.compile(r"\{\{(\w+)\}\}")


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
    Construye el prompt final para un GEM de forma eficiente.

    1. Carga el prompt del GEM y el maestro (desde caché si es posible).
    2. Inyecta {{PROMPT_MAESTRO}} en el prompt del GEM.
    3. Reemplaza todas las {{variables}} en una sola pasada usando regex.
    4. Valida que no queden variables críticas sin reemplazar.

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (uso de caché para evitar E/S de disco repetitiva)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro (primera pasada para que el maestro también pueda tener variables)
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    def replace_var(match):
        key = match.group(1)
        if key == "VERSION":
            return match.group(0)  # Mantener {{VERSION}} como metadata

        value = variables.get(key)
        if value is None:
            return match.group(0)  # Mantener placeholder si no hay valor

        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False, indent=2)
        return str(value)

    # Sustitución de variables en una sola pasada usando regex pre-compilado
    prompt = VARIABLE_PATTERN.sub(replace_var, prompt)

    # Validar que no queden variables sin reemplazar (excepto VERSION)
    remaining = VARIABLE_PATTERN.findall(prompt)
    if remaining:
        remaining = [v for v in remaining if v != "VERSION"]
        if remaining:
            # Importación local para evitar dependencias circulares si logger usara prompt_builder
            from agent.logger import logger
            logger.warning(f"⚠️  Variables sin reemplazar en {gem_name}: {remaining}")

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
