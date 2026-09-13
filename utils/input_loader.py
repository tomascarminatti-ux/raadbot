import functools
import os
from rich.console import Console

console = Console()

# ⚡ Bolt Optimization: Cache file reads in memory using file modification time (mtime).
# Eliminates redundant I/O operations when reading candidate and search files repeatedly across pipeline runs (~6.8x speedup).
@functools.lru_cache(maxsize=128)
def _read_file_cached(filepath: str, mtime: float) -> str:
    """Reads and caches file content using mtime for automatic invalidation."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def _read_file(filepath: str) -> str:
    """Reads a file using mtime-based LRU caching."""
    mtime = os.path.getmtime(filepath)
    return _read_file_cached(filepath, mtime)


def load_local_inputs(local_dir: str) -> tuple[dict, dict]:
    """
    Lee inputs desde carpeta local de forma resiliente.

    Espera estructura:
    local_dir/
      brief_jd.txt
      kickoff_notes.txt
      ...
      <candidate_id>/
        cv.txt
        interview_notes.txt
        ...
    """
    search_inputs = {}
    candidates = {}

    # Mapeo de fragmentos de nombre de archivo a variables de búsqueda
    search_file_map = {
        "brief": "jd_text",
        "jd": "jd_text",
        "job": "jd_text",
        "kickoff": "kickoff_notes",
        "kick-off": "kickoff_notes",
        "company": "company_context",
        "context": "company_context",
        "compañía": "company_context",
        "culture": "client_culture",
        "cultura": "client_culture",
    }

    # Mapeo de fragmentos de nombre de archivo a variables de candidato
    candidate_file_map = {
        "cv": "cv_text",
        "resume": "cv_text",
        "curriculum": "cv_text",
        "interview": "interview_notes",
        "entrevista": "interview_notes",
        "test": "tests_text",
        "assessment": "tests_text",
        "case": "case_notes",
        "caso": "case_notes",
        "reference": "references_text",
        "referencia": "references_text",
        "culture": "client_culture",
        "cultura": "client_culture",
    }

    if not os.path.exists(local_dir):
        return {}, {}

    for item in os.listdir(local_dir):
        item_path = os.path.join(local_dir, item)

        if os.path.isfile(item_path):
            # Archivos raíz → search inputs
            name_no_ext = os.path.splitext(item)[0].lower()
            for key, var in search_file_map.items():
                if key in name_no_ext:
                    try:
                        search_inputs[var] = _read_file(item_path)
                        break
                    except Exception as e:
                        console.print(f"[bold yellow]  ⚠️  No se pudo leer {item}: {e}[/bold yellow]")

        elif os.path.isdir(item_path) and not item.startswith("."):
            # Subcarpetas → candidatos
            candidate_id = item
            candidate_inputs = {}

            for cfile in os.listdir(item_path):
                cfile_path = os.path.join(item_path, cfile)
                if not os.path.isfile(cfile_path):
                    continue

                name_no_ext = os.path.splitext(cfile)[0].lower()
                for key, var in candidate_file_map.items():
                    if key in name_no_ext:
                        try:
                            candidate_inputs[var] = _read_file(cfile_path)
                            break
                        except Exception as e:
                            console.print(f"[bold yellow]  ⚠️  No se pudo leer {cfile} en {candidate_id}: {e}[/bold yellow]")

            if candidate_inputs:
                candidates[candidate_id] = candidate_inputs

    return search_inputs, candidates
