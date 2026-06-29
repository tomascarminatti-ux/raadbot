"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import json
from functools import lru_cache


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
# Patrón para encontrar {{variable}}
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


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


@lru_cache(maxsize=32)
def _get_template_with_maestro(gem_name: str) -> str:
    """
    Obtiene el template del GEM con el PROMPT_MAESTRO ya inyectado.
    Optimiza la construcción evitando lecturas de disco y reemplazos.
    """
    maestro = load_maestro()
    prompt = load_prompt(gem_name)
    return prompt.replace("{{PROMPT_MAESTRO}}", maestro)


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el prompt (cacheado) con el maestro inyectado.
    2. Reemplaza todas las {{variables}} en un solo paso usando regex.
    3. Valida que no queden variables sin reemplazar.

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Obtener template base con maestro ya inyectado (cacheado)
    prompt = _get_template_with_maestro(gem_name)

    # Preparar mapeo de variables (serializar dicts si es necesario)
    var_map = {}
    for k, v in variables.items():
        if isinstance(v, dict):
            var_map[k] = json.dumps(v, ensure_ascii=False, indent=2)
        else:
            var_map[k] = str(v)

    def replace_func(match):
        var_name = match.group(1)
        return var_map.get(var_name, match.group(0))

    prompt = VAR_PATTERN.sub(replace_func, prompt)

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
    Extrae las variables requeridas de un prompt.

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
    """Helper genérico para construir prompts de agentes con inyección."""
    base_prompt = load_prompt(gem_id)
    # Intentamos inyectar en {{input}} o {{context}}
    prompt = build_prompt(gem_id, {"input": payload, "context": payload})

    # Si no hay placeholder de datos, los anexamos al final
    if "{{input}}" not in base_prompt and "{{context}}" not in base_prompt:
        data_json = json.dumps(payload, ensure_ascii=False, indent=2)
        prompt += f"\n\n### DATA INPUT:\n{data_json}"

    return prompt
