"""
prompt_builder.py – Construye prompts finales inyectando variables de template.
"""

import os
import re
import functools
import json

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


def _get_file_mtime(filepath: str) -> float:
    """Returns the modification time of a file to check if cache needs to be invalidated."""
    try:
        return os.path.getmtime(filepath)
    except OSError:
        return 0.0


@functools.lru_cache(maxsize=32)
def _load_prompt_cached(gem_name: str, mtime: float) -> str:
    """Helper that actually loads the file, cached by both filename and mtime."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_prompt(gem_name: str) -> str:
    """Carga un prompt desde el directorio de prompts (con invalidación de caché automática si cambia mtime)."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)
    mtime = _get_file_mtime(filepath)
    return _load_prompt_cached(gem_name, mtime)


def load_maestro() -> str:
    """Carga el prompt maestro."""
    return load_prompt("00_prompt_maestro")


@functools.lru_cache(maxsize=128)
def _compile_regex(pattern: str):
    return re.compile(pattern)


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
    # Cargar prompt maestro y del GEM
    maestro = load_maestro()
    prompt = load_prompt(gem_name)

    # Inyectar prompt maestro
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)

    # Inyectar variables with single-pass replacement optimization
    if variables:
        # Pre-process dicts to json strings to avoid repeating in the replacement loop
        processed_vars = {}
        for k, v in variables.items():
            if isinstance(v, dict):
                processed_vars[k] = json.dumps(v, ensure_ascii=False, indent=2)
            else:
                processed_vars[k] = str(v)

        # Build single regex pattern for all variable keys, sorted by length descending to prevent prefix matching conflicts
        sorted_keys = sorted(processed_vars.keys(), key=len, reverse=True)
        pattern_str = "|".join(re.escape("{{" + k + "}}") for k in sorted_keys)
        pattern = _compile_regex(pattern_str)

        # Single-pass replace function
        def repl(match):
            placeholder = match.group(0)
            key = placeholder[2:-2]
            return processed_vars.get(key, placeholder)

        prompt = pattern.sub(repl, prompt)

    # Validar que no queden variables sin reemplazar
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
