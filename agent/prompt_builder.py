"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
Optimizado para rendimiento (Bolt ⚡).
"""

import os
import re
import json
from functools import lru_cache


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

# Pre-compilar el patrón de variables a nivel de módulo para evitar recompilaciones repetidas
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


@lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (con caché para evitar lecturas de disco)."""
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


def clear_prompt_caches():
    """Limpia la caché de prompts tras refinamientos."""
    load_prompt.cache_clear()
    load_maestro.cache_clear()


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM de forma altamente eficiente.

    1. Carga el prompt del GEM y el maestro utilizando caché.
    2. Inyecta {{PROMPT_MAESTRO}}
    3. Reemplaza variables en una única pasada con re.sub para optimizar rendimiento.
    4. Valida que no queden variables sin reemplazar.

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (usando lru_cache)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Procesar variables (conversión a strings) por adelantado
    processed_vars = {}
    for key, val in variables.items():
        if isinstance(val, dict):
            processed_vars[key] = json.dumps(val, ensure_ascii=False, indent=2)
        else:
            processed_vars[key] = str(val)

    # Reemplazo de variables en una única pasada de O(N)
    def replacer(match):
        var_name = match.group(1)
        # Si la variable está en el diccionario de variables, la reemplazamos;
        # de lo contrario, la dejamos intacta (ej: {{VERSION}})
        return processed_vars.get(var_name, match.group(0))

    prompt = VAR_PATTERN.sub(replacer, prompt)

    # Validar que no queden variables sin reemplazar
    remaining = VAR_PATTERN.findall(prompt)
    if remaining:
        # Filtrar VERSION que es metadata, no un input
        remaining = [v for v in remaining if v != "VERSION"]
        if remaining:
            print(f"  ⚠️  Variables sin reemplazar: {remaining}")

    return prompt


def get_required_variables(gem_name: str) -> list[str]:
    """
    Extrae las variables requeridas de un prompt de manera eficiente.

    Returns:
        Lista de nombres de variables (sin {{ }})
    """
    prompt = load_prompt(gem_name)
    variables = VAR_PATTERN.findall(prompt)
    # Filtrar las que se resuelven automáticamente
    auto_resolved = {"PROMPT_MAESTRO", "VERSION"}
    return [v for v in set(variables) if v not in auto_resolved]
