"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import json
from functools import lru_cache


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


@lru_cache(maxsize=32)
def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (Cacheado)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@lru_cache(maxsize=1)
def load_maestro() -> str:
    """Carga el prompt maestro (Cacheado)."""
    return load_prompt("00_prompt_maestro")


@lru_cache(maxsize=32)
def _get_template_with_maestro(gem_name: str) -> str:
    """Combina el prompt del GEM con el maestro (Cacheado)."""
    maestro = load_maestro()
    prompt = load_prompt(gem_name)
    return prompt.replace("{{PROMPT_MAESTRO}}", maestro)


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM optimizado para velocidad.

    1. Recupera template con maestro de caché
    2. Realiza inyección de variables en un solo paso regex
    3. Valida variables restantes

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    prompt = _get_template_with_maestro(gem_name)

    def _replace(match):
        key = match.group(1)
        if key in variables:
            val = variables[key]
            if isinstance(val, dict):
                return json.dumps(val, ensure_ascii=False, indent=2)
            return str(val)
        return match.group(0)  # Dejar el placeholder si no está en variables

    # Inyectar variables en un solo paso
    prompt = VAR_PATTERN.sub(_replace, prompt)

    # Validar que no queden variables sin reemplazar (excluyendo metadata)
    remaining = VAR_PATTERN.findall(prompt)
    if remaining:
        remaining = [v for v in remaining if v not in ("VERSION", "PROMPT_MAESTRO")]
        if remaining:
            print(f"  ⚠️  Variables sin reemplazar en {gem_name}: {remaining}")

    return prompt


def get_required_variables(gem_name: str) -> list[str]:
    """
    Extrae las variables requeridas de un prompt.

    Returns:
        Lista de nombres de variables (sin {{ }})
    """
    prompt = load_prompt(gem_name)
    variables = re.findall(r"\{\{(\w+)\}\}", prompt)
    # Filtrar las que se resuelven automáticamente
    auto_resolved = {"PROMPT_MAESTRO", "VERSION"}
    return [v for v in set(variables) if v not in auto_resolved]
