"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import json
import functools


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


@functools.lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (con caché)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@functools.lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro (con caché)."""
    return load_prompt("00_prompt_maestro")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el prompt del GEM
    2. Inyecta {{PROMPT_MAESTRO}}
    3. Reemplaza todas las {{variables}} en una sola pasada regex
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (desde caché)
    maestro = load_maestro()
    template = load_prompt(gem_name)

    # Inyectar prompt maestro primero para permitir variables dentro de él
    prompt = template.replace("{{PROMPT_MAESTRO}}", maestro)

    # Preparar mapa de reemplazo incluyendo variables y VERSION (si no se provee)
    # VERSION suele ser metadata estática en el prompt, pero la lógica original
    # la filtraba al final. Aquí simplemente no la tocamos si no está en variables.

    def replacement_handler(match):
        key = match.group(1)
        if key == "PROMPT_MAESTRO":
            return maestro # Ya reemplazado arriba, pero por si acaso

        if key in variables:
            val = variables[key]
            if isinstance(val, dict):
                return json.dumps(val, ensure_ascii=False, indent=2)
            return str(val)

        # Si es VERSION u otra no proveída, la dejamos como está para el check final
        return "{{" + key + "}}"

    # Reemplazo en una sola pasada
    prompt = VAR_PATTERN.sub(replacement_handler, prompt)

    # Validar que no queden variables sin reemplazar
    remaining = VAR_PATTERN.findall(prompt)
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
    variables = VAR_PATTERN.findall(prompt)
    # Filtrar las que se resuelven automáticamente
    auto_resolved = {"PROMPT_MAESTRO", "VERSION"}
    return [v for v in set(variables) if v not in auto_resolved]
