"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import functools

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

# Precompiled regex pattern at the module level for optimal replacement performance.
# Minimizes the overhead of compiling regexes repeatedly in a loop.
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


# Bolt Optimization: Caching loaded prompts with LRU cache avoids redundant Disk I/O
# and significantly speeds up multiple prompt builds across evaluations/runs.
@functools.lru_cache(maxsize=16)
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


# Bolt Optimization: Manual cache invalidation function for prompt refinements.
def clear_prompt_caches():
    """Limpia la cache de carga de prompts."""
    load_prompt.cache_clear()


def build_prompt(gem_name: str, variables: dict) -> str:
    """
    Construye el prompt final para un GEM.

    1. Carga el prompt del GEM (cached)
    2. Inyecta {{PROMPT_MAESTRO}} (cached)
    3. Reemplaza todas las {{variables}} in a single pass using re.sub for maximum speed.
    4. Valida que no queden variables sin reemplazar

    Args:
        gem_name: nombre del GEM (ej: "gem1", "gem5")
        variables: dict con las variables a inyectar

    Returns:
        str con el prompt listo para enviar al modelo
    """
    # Cargar prompt maestro y del GEM (both are loaded via cached load_prompt)
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Pre-format dictionary variable values to formatted JSON strings to avoid repeat serialization in loop.
    formatted_vars = {}
    for key, value in variables.items():
        if isinstance(value, dict):
            import json
            formatted_vars[key] = json.dumps(value, ensure_ascii=False, indent=2)
        else:
            formatted_vars[key] = str(value)

    # Single-pass substitution of variables.
    # Instead of iterating through all keys and doing string replace, this executes in a single pass
    # which scales O(N) with prompt length rather than O(K * N) where K is the number of keys.
    def replacer(match):
        var_name = match.group(1)
        return formatted_vars.get(var_name, match.group(0))

    prompt = VAR_PATTERN.sub(replacer, prompt)

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
