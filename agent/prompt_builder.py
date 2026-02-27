"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import functools
import json
import os
import re


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


@functools.lru_cache()
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts."""
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
    Construye el prompt final para un GEM.

    1. Carga el prompt del GEM y el maestro.
    2. Inyecta {{PROMPT_MAESTRO}} (soporta nesting).
    3. Pre-serializa variables complejas (dicts/lists) a JSON.
    4. Reemplaza todas las {{ variables }} en una sola pasada usando regex.
    5. Valida variables faltantes durante la sustitución.

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro primero (puede contener placeholders)
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Pre-serializar variables para evitar JSON dumps repetidos
    processed_vars = {}
    for k, v in variables.items():
        if isinstance(v, (dict, list)):
            processed_vars[k] = json.dumps(v, ensure_ascii=False, indent=2)
        else:
            processed_vars[k] = str(v)

    missing_vars = []

    def replacer(match):
        key = match.group(1).strip()
        if key in processed_vars:
            return processed_vars[key]
        if key == "VERSION":
            return match.group(0)
        missing_vars.append(key)
        return match.group(0)

    # Sustitución en una sola pasada con soporte para espacios opcionales
    prompt = re.sub(r"\{\{\s*(.*?)\s*\}\}", replacer, prompt)

    if missing_vars:
        # Filtrar duplicados y reportar
        unique_missing = sorted(list(set(missing_vars)))
        print(f"  ⚠️  Variables sin reemplazar en {gem_name}: {unique_missing}")

    return prompt


def get_required_variables(gem_name: str) -> list[str]:
    """
    Extrae las variables requeridas de un prompt.

    Returns:
        Lista de nombres de variables (sin {{ }})
    """
    prompt = load_prompt(gem_name)
    # Regex robusta que ignora espacios
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
    # Usamos regex para ser consistentes con build_prompt y soportar espacios
    has_input = re.search(r"\{\{\s*input\s*\}\}", base_prompt)
    has_context = re.search(r"\{\{\s*context\s*\}\}", base_prompt)

    if not has_input and not has_context:
        # build_prompt ya se encargó del grueso, pero si el template no tenía placeholders
        # y queremos forzar la inclusión de la data:
        data_str = json.dumps(payload, ensure_ascii=False, indent=2)
        prompt += f"\n\n### DATA INPUT:\n{data_str}"

    return prompt
