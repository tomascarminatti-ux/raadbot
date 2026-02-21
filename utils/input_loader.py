import os
from rich.console import Console

console = Console()

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
                        with open(item_path, "r", encoding="utf-8") as f:
                            search_inputs[var] = f.read()
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
                            with open(cfile_path, "r", encoding="utf-8") as f:
                                candidate_inputs[var] = f.read()
                            break
                        except Exception as e:
                            console.print(f"[bold yellow]  ⚠️  No se pudo leer {cfile} en {candidate_id}: {e}[/bold yellow]")

            if candidate_inputs:
                candidates[candidate_id] = candidate_inputs

    return search_inputs, candidates
