"""
prompt_builder.py – Construye prompts finales inyectando variables de template de manera optimizada.
"""

import os
import re
import json
import functools

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


@functools.lru_cache(maxsize=32)
def _load_prompt_cached(gem_name: str, mtime: float) -> str:
    """
    Carga y cachea el contenido de un prompt basado en su nombre y el mtime del archivo.
    Si el archivo cambia en disco, el mtime cambiará y se generará una nueva entrada de caché.
    """
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (con caché basada en mtime)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    # Obtener mtime sin decorar con lru_cache para asegurar detección instantánea de cambios
    mtime = os.path.getmtime(filepath)
    return _load_prompt_cached(gem_name, mtime)


def load_maestro() -> str:
    """Carga el prompt maestro."""
    return load_prompt("00_prompt_maestro")


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM de forma altamente optimizada.

    1. Carga el prompt del GEM y el maestro desde la caché basada en mtime
    2. Inyecta {{PROMPT_MAESTRO}} primero (con .replace() tradicional para que placeholders anidados se resuelvan luego)
    3. Reemplaza todas las {{variables}} de manera eficiente en una sola pasada usando re.sub
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # 1. Cargar prompts desde caché
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # 2. Inyectar prompt maestro primero con .replace() para que placeholders anidados se resuelvan luego
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # 3. Inyectar variables en una sola pasada eficiente
    if variables:
        processed_vars = {}
        for key, value in variables.items():
            if isinstance(value, dict):
                processed_vars[key] = json.dumps(value, ensure_ascii=False, indent=2)
            else:
                processed_vars[key] = str(value)

        # Ordenar llaves por longitud descendente para evitar conflictos de coincidencia parcial de prefijos
        sorted_keys = sorted(processed_vars.keys(), key=len, reverse=True)
        escaped_keys = [re.escape(k) for k in sorted_keys]
        pattern = re.compile(r"\{\{(" + "|".join(escaped_keys) + r")\}\}")

        # Reemplazar usando re.sub en una sola pasada
        prompt = pattern.sub(lambda match: processed_vars[match.group(1)], prompt)

    # 4. Validar que no queden variables sin reemplazar
    remaining = re.findall(r"\{\{(\w+)\}\}", prompt)
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
    variables = re.findall(r"\{\{(\w+)\}\}", prompt)
    # Filtrar las que se resuelven automáticamente
    auto_resolved = {"PROMPT_MAESTRO", "VERSION"}
    return [v for v in set(variables) if v not in auto_resolved]


def clear_prompt_caches():
    """Limpia de forma manual las cachés de templates."""
    _load_prompt_cached.cache_clear()
