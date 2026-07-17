"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import json
import functools

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

# Pre-compile regular expressions at the module level to minimize runtime overhead
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


@functools.lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (con lru_cache para eliminar I/O repetitivo)."""
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


def clear_prompt_caches():
    """Limpia los caches de prompts para forzar la recarga desde el disco (útil tras refinamientos)."""
    load_prompt.cache_clear()
    load_maestro.cache_clear()


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM de manera optimizada y eficiente.

    1. Carga el prompt del GEM y el maestro (usando lru_cache)
    2. Inyecta {{PROMPT_MAESTRO}} para resolver templates anidados
    3. Reemplaza variables en un solo paso mediante re.sub y un callback de diccionario
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (desde caché lru)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro primero para permitir resoluciones anidadas
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # callback optimizado para reemplazo en un solo paso
    def replace_match(match):
        var_name = match.group(1)
        # El tag VERSION es metadata del prompt y se maneja por fuera
        if var_name == "VERSION":
            return match.group(0)
        if var_name in variables:
            val = variables[var_name]
            if isinstance(val, dict):
                return json.dumps(val, ensure_ascii=False, indent=2)
            return str(val)
        return match.group(0)

    prompt = VAR_PATTERN.sub(replace_match, prompt)

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
