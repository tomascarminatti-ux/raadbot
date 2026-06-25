"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
Optimizado por Bolt ⚡ para rendimiento máximo mediante caching y re.sub().
"""

import os
import re
import json
from functools import lru_cache


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

# Regex pre-compilada para inyección de variables
# Soporta {{variable}} con caracteres alfanuméricos y guion bajo
VAR_PATTERN = re.compile(r"\{\{([a-zA-Z0-9_-]+)\}\}")


@lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts con cache en memoria."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_maestro() -> str:
    """Carga el prompt maestro."""
    return load_prompt("00_prompt_maestro")


@lru_cache(maxsize=32)
def get_template_base(gem_name: str) -> str:
    """
    Obtiene el template base (Maestro + GEM) con cache para evitar inyecciones repetitivas.
    """
    maestro = load_maestro()
    prompt = load_prompt(gem_name)
    # Inyectar prompt maestro (solo se hace una vez por GEM gracias al lru_cache)
    return prompt.replace("{{PROMPT_MAESTRO}}", maestro)


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el template base (Maestro + GEM) desde cache.
    2. Inyecta todas las {{variables}} en una sola pasada usando regex.
    3. Valida que no queden variables sin reemplazar.

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    prompt = get_template_base(gem_name)

    # Inyectar variables en una sola pasada (O(N) vs O(N*M))
    def replace_var(match):
        key = match.group(1)
        if key in variables:
            value = variables[key]
            if isinstance(value, (dict, list)):
                return json.dumps(value, ensure_ascii=False, indent=2)
            return str(value)
        return match.group(0)  # Mantener {{key}} si no está en variables

    prompt = VAR_PATTERN.sub(replace_var, prompt)

    # Validar que no queden variables sin reemplazar
    remaining = VAR_PATTERN.findall(prompt)
    if remaining:
        # Filtrar VERSION que es metadata, no un input
        remaining = [v for v in remaining if v != "VERSION"]
        if remaining:
            # Importado aquí para evitar ruidos en ejecución normal si no es crítico
            from agent.logger import logger
            logger.warning(f"⚠️ Variables sin reemplazar en {gem_name}: {remaining}")

    return prompt


def get_required_variables(gem_name: str) -> list[str]:
    """
    Extrae las variables requeridas de un prompt.

    Returns:
        Lista de nombres de variables (sin {{ }})
    """
    prompt = load_prompt(gem_name)
    variables = VAR_PATTERN.findall(prompt)
    # Filtrar las que se resuelven automáticamente
    auto_resolved = {"PROMPT_MAESTRO", "VERSION"}
    return list(set(v for v in variables if v not in auto_resolved))
