"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import json
from functools import lru_cache


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


@lru_cache
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

    1. Carga el prompt del GEM
    2. Inyecta {{PROMPT_MAESTRO}}
    3. Reemplaza todas las {{variables}} en un solo paso
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Pre-procesar variables: serializar dicts/lists a JSON una sola vez
    processed_vars = {"PROMPT_MAESTRO": maestro}
    for k, v in variables.items():
        if isinstance(v, (dict, list)):
            processed_vars[k] = json.dumps(v, ensure_ascii=False, indent=2)
        else:
            processed_vars[k] = str(v)

    # Reemplazo en un solo paso usando regex con soporte para espacios
    pattern = re.compile(r"\{\{\s*(.*?)\s*\}\}")

    def replace_func(match):
        var_name = match.group(1)
        # Soporte para nesting (PROMPT_MAESTRO suele contener placeholders)
        if var_name == "PROMPT_MAESTRO":
            # Si el maestro tiene placeholders, serán resueltos por el mismo sub pass
            # Pero re.sub no es recursivo por defecto.
            # Sin embargo, maestro se inyecta y sus variables DEBEN estar en variables dict.
            return processed_vars.get(var_name, match.group(0))
        return processed_vars.get(var_name, match.group(0))

    # Realizamos una pasada para inyectar el maestro primero si existe,
    # para que sus placeholders sean visibles en la pasada final.
    if "{{PROMPT_MAESTRO}}" in prompt or re.search(r"\{\{\s*PROMPT_MAESTRO\s*\}\}", prompt):
        prompt = re.sub(r"\{\{\s*PROMPT_MAESTRO\s*\}\}", maestro, prompt)

    # Pasada final para todas las variables
    prompt = pattern.sub(replace_func, prompt)

    # Validar que no queden variables sin reemplazar (ignorando metadata)
    remaining = pattern.findall(prompt)
    if remaining:
        # Filtrar VERSION que es metadata, no un input
        remaining = [v for v in remaining if v != "VERSION" and v != "PROMPT_MAESTRO"]
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
    variables = re.findall(r"\{\{\s*(.*?)\s*\}\}", prompt)
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
    # Usamos regex para ser consistentes con la flexibilidad de espacios de build_prompt
    has_input = re.search(r"\{\{\s*input\s*\}\}", base_prompt)
    has_context = re.search(r"\{\{\s*context\s*\}\}", base_prompt)

    if not has_input and not has_context:
        prompt += f"\n\n### DATA INPUT:\n{json.dumps(payload, ensure_ascii=False, indent=2)}"

    return prompt
