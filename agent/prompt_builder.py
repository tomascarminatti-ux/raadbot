"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
Optimizado con caching LRU para reducir I/O de disco y substitución regex de un solo paso.
"""

import os
import re
from functools import lru_cache

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

# Regex pre-compilado a nivel de módulo para evitar recompilación en cada llamada
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


@lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts. Cacheado con LRU."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro. Cacheado con LRU."""
    return load_prompt("00_prompt_maestro")


def clear_prompt_caches():
    """Limpia los cachés de prompts cargados. Debe llamarse cuando un prompt se actualiza/refina."""
    load_prompt.cache_clear()
    load_maestro.cache_clear()


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el prompt del GEM (con caché)
    2. Inyecta {{PROMPT_MAESTRO}} (con caché)
    3. Reemplaza todas las {{variables}} (sustitución en un solo paso con re.sub)
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (ambos usan caché LRU para evitar I/O)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Serializar variables y preparar un diccionario para sustitución regex de un paso
    vars_dict = {}
    for key, value in variables.items():
        if isinstance(value, dict):
            import json
            value_str = json.dumps(value, ensure_ascii=False, indent=2)
        else:
            value_str = str(value)
        vars_dict[key] = value_str

    # Callback para re.sub que realiza reemplazo en un solo paso
    def replace_var(match):
        var_name = match.group(1)
        if var_name == "VERSION":
            return match.group(0)  # Dejar {{VERSION}} intacto
        if var_name in vars_dict:
            return vars_dict[var_name]
        return match.group(0)  # Dejar placeholder faltante intacto

    prompt = VAR_PATTERN.sub(replace_var, prompt)

    # Validar que no queden variables sin reemplazar usando el regex pre-compilado
    remaining = VAR_PATTERN.findall(prompt)
    if remaining:
        # Filtrar VERSION que es metadata, no un input
        remaining = [v for v in remaining if v != "VERSION"]
        if remaining:
            print(f"  ⚠️  Variables sin reemplazar: {remaining}")

    return prompt


def get_required_variables(gem_name: str) -> list[str]:
    """
    Extrae las variables requeridas de un prompt usando regex pre-compilado.

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
