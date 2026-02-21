"""
utils.py – Utilidades para carga de archivos y manejo de datos.
"""

import os

def load_local_inputs(local_dir: str) -> tuple[dict, dict]:
    """
    Lee inputs desde carpeta local.

    Espera estructura:
    local_dir/
      brief_jd.txt
      kickoff_notes.txt
      company_context.txt
      <candidate_id>/
        cv.txt
        interview_notes.txt
        tests.txt
        case_notes.txt
        references.txt
        client_culture.txt
    """
    search_inputs = {}
    candidates = {}

    # Mapeo de nombres de archivo a variables
    search_file_map = {
        "brief_jd": "jd_text",
        "jd": "jd_text",
        "brief": "jd_text",
        "kickoff_notes": "kickoff_notes",
        "kickoff": "kickoff_notes",
        "company_context": "company_context",
        "company": "company_context",
        "client_culture": "client_culture",
        "culture": "client_culture",
    }

    candidate_file_map = {
        "cv": "cv_text",
        "resume": "cv_text",
        "curriculum": "cv_text",
        "interview_notes": "interview_notes",
        "interview": "interview_notes",
        "entrevista": "interview_notes",
        "tests": "tests_text",
        "test": "tests_text",
        "assessment": "tests_text",
        "case_notes": "case_notes",
        "case": "case_notes",
        "caso": "case_notes",
        "references": "references_text",
        "referencia": "references_text",
        "referencias": "references_text",
        "client_culture": "client_culture",
        "culture": "client_culture",
        "cultura": "client_culture",
    }

    if not os.path.exists(local_dir):
        raise FileNotFoundError(f"Directorio local no encontrado: {local_dir}")

    for item in os.listdir(local_dir):
        item_path = os.path.join(local_dir, item)

        if os.path.isfile(item_path):
            # Archivos raíz → search inputs
            name_no_ext = os.path.splitext(item)[0].lower()
            for key, var in search_file_map.items():
                if key in name_no_ext:
                    with open(item_path, "r", encoding="utf-8") as f:
                        search_inputs[var] = f.read()
                    break

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
                        with open(cfile_path, "r", encoding="utf-8") as f:
                            candidate_inputs[var] = f.read()
                        break

            if candidate_inputs:
                candidates[candidate_id] = candidate_inputs

    return search_inputs, candidates
