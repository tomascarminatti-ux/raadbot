"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import functools


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
    import json

    # Cargar prompt maestro y del GEM
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Preparar mapeo de variables
    replacements = {}
    for key, value in variables.items():
        if isinstance(value, dict):
            replacements[key] = json.dumps(value, ensure_ascii=False, indent=2)
        else:
            replacements[key] = str(value)

    # El prompt maestro puede contener variables que deben ser reemplazadas.
    # Primero inyectamos el maestro en el prompt del GEM.
    # Usamos replace simple para el maestro ya que es un placeholder fijo y conocido.
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Reemplazo en una sola pasada usando re.sub para todas las variables
    pattern = re.compile(r"\{\{\s*(\w+)\s*\}\}")

    def replace_match(match):
        var_name = match.group(1)
        return replacements.get(var_name, match.group(0))

    prompt = pattern.sub(replace_match, prompt)

    # Validar que no queden variables sin reemplazar
    remaining = pattern.findall(prompt)
    if remaining:
        # Filtrar VERSION que es metadata, no un input
        remaining = [v for v in remaining if v != "VERSION"]
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
        import json
        # Usamos el prompt ya procesado para anexar
        prompt += f"\n\n### DATA INPUT:\n{json.dumps(payload, ensure_ascii=False, indent=2)}"

    return prompt
