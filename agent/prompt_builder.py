"""
prompt_builder.py – Construye prompts finales inyectando variables de template de forma eficiente.
"""

import os
import re
import json
from functools import lru_cache


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
# Pre-compilar patrón de variables para mayor velocidad
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
    Obtiene el template del GEM con el Maestro ya inyectado.
    Cachamos este resultado intermedio para evitar múltiples concatenaciones.
    """
    maestro = load_maestro()
    prompt = load_prompt(gem_name)
    return prompt.replace("{{PROMPT_MAESTRO}}", maestro)


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el template base (Maestro + GEM) desde caché
    2. Reemplaza variables en una sola pasada usando re.sub con callback
    3. Valida variables faltantes durante el mismo proceso

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    template = _get_template_with_maestro(gem_name)

    missing = []

    def _replace_callback(match):
        var_name = match.group(1)
        if var_name in variables:
            value = variables[var_name]
            if isinstance(value, dict):
                return json.dumps(value, ensure_ascii=False, indent=2)
            return str(value)

        # VERSION es metadata opcional, no disparamos alerta
        if var_name == "VERSION":
            return match.group(0)

        missing.append(var_name)
        return match.group(0)

    # Reemplazo ultra-rápido en una sola pasada
    prompt = VAR_PATTERN.sub(_replace_callback, template)

    if missing:
        # Usamos set para no repetir variables en el log
        logger_warn = list(set(missing))
        print(f"  ⚠️  Variables sin reemplazar: {logger_warn}")

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
