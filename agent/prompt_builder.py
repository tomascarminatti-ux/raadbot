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
    """Carga un prompt desde el directorio de prompts (con caché)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_maestro() -> str:
    """Carga el prompt maestro."""
    return load_prompt("00_prompt_maestro")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM (Optimizado).

    1. Carga el prompt del GEM (cacheado)
    2. Inyecta {{PROMPT_MAESTRO}}
    3. Reemplaza todas las {{variables}} en una sola pasada de regex
    4. Valida que no queden variables críticas sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro primero
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Pre-serializar variables para evitar múltiples llamadas a json.dumps
    serialized_vars = {}
    for k, v in variables.items():
        if isinstance(v, (dict, list)):
            serialized_vars[k] = json.dumps(v, ensure_ascii=False, indent=2)
        else:
            serialized_vars[k] = str(v)

    # Sustitución eficiente en una sola pasada usando regex (soporta espacios)
    pattern = re.compile(r"\{\{\s*(\w+)\s*\}\}")

    def replace_func(match):
        var_name = match.group(1)
        if var_name in serialized_vars:
            return serialized_vars[var_name]
        return match.group(0) # Mantener si no se encuentra (ej: VERSION)

    prompt = pattern.sub(replace_func, prompt)

    # Validar que no queden variables sin reemplazar (ignorando metadatos conocidos)
    remaining = pattern.findall(prompt)
    if remaining:
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
    variables = re.findall(r"\{\{\s*(\w+)\s*\}\}", prompt)
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
        prompt += f"\n\n### DATA INPUT:\n{json.dumps(payload, ensure_ascii=False, indent=2)}"

    return prompt
