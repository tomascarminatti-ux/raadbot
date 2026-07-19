"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
from functools import lru_cache

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

# Pre-compilar el patrón de variables a nivel de módulo para optimizar el rendimiento
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


@lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (con cache LRU)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro (con cache LRU)."""
    return load_prompt("00_prompt_maestro")


def clear_prompt_caches():
    """Invalida manualmente la caché LRU para load_prompt y load_maestro."""
    load_prompt.cache_clear()
    load_maestro.cache_clear()


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM de forma altamente optimizada.

    1. Carga el prompt del GEM (desde cache LRU)
    2. Inyecta {{PROMPT_MAESTRO}} (desde cache LRU)
    3. Reemplaza todas las {{variables}} en un solo paso con re.sub
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (aprovechando caché)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Inyectar variables en una sola pasada de expresión regular
    def replace_match(match):
        var_name = match.group(1)
        if var_name == "VERSION":
            return match.group(0)  # Conservar VERSION para metadatos
        if var_name in variables:
            val = variables[var_name]
            if isinstance(val, dict):
                import json
                return json.dumps(val, ensure_ascii=False, indent=2)
            return str(val) if val is not None else ""
        return match.group(0)  # No tocar variables que falten en el diccionario

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
    Extrae las variables requeridas de un prompt usando patrón pre-compilado.

    Returns:
        Lista de nombres de variables (sin {{ }})
    """
    prompt = load_prompt(gem_name)
    variables = VAR_PATTERN.findall(prompt)
    # Filtrar las que se resuelven automáticamente
    auto_resolved = {"PROMPT_MAESTRO", "VERSION"}
    return [v for v in set(variables) if v not in auto_resolved]


def build_gem5_prompt(search_inputs: dict) -> str:
    """Helper para construir el prompt de GEM 5 (usado en api.py)."""
    return build_prompt("gem5", {"input": search_inputs})


def build_agent_prompt(gem_id: str, payload: dict) -> str:
    """Helper genérico para construir prompts de agentes con inyección de datos."""
    base_prompt = load_prompt(gem_id)
    # Intentamos inyectar en {{input}} o {{context}}
    prompt = build_prompt(gem_id, {"input": payload, "context": payload})

    # Si no se encontró ningún placeholder de datos en el prompt original, los anexamos al final
    if "{{input}}" not in base_prompt and "{{context}}" not in base_prompt:
        import json
        prompt += f"\n\n### DATA INPUT:\n{json.dumps(payload, ensure_ascii=False, indent=2)}"

    return prompt
