#!/usr/bin/env python3
"""
run.py – Entry point para el pipeline RAAD GEM.

Uso:
    # Con Google Drive
    python run.py --search-id SEARCH-2026-001 --drive-folder <FOLDER_ID>

    # Con carpeta local
    python run.py --search-id SEARCH-2026-001 --local-dir runs/SEARCH-2026-001/inputs

    # Solo un candidato
    python run.py --search-id SEARCH-2026-001 --local-dir ./inputs --candidate CAND-001
"""

import argparse
import json
import os
import sys

from dotenv import load_dotenv


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


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="RAAD GEM Pipeline – Evaluación de candidatos ejecutivos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python run.py --search-id SEARCH-2026-001 --local-dir runs/SEARCH-2026-001/inputs
  python run.py --search-id SEARCH-2026-001 --drive-folder 1aBcDeFgHiJkLmNoPqRsT
  python run.py --search-id SEARCH-2026-001 --local-dir ./inputs --candidate CAND-001
        """,
    )

    parser.add_argument(
        "--search-id",
        required=True,
        help="ID de la búsqueda (ej: SEARCH-2026-001)",
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--local-dir",
        help="Carpeta local con inputs (ver README para estructura)",
    )
    source.add_argument(
        "--drive-folder",
        help="ID de carpeta de Google Drive con inputs",
    )

    parser.add_argument(
        "--candidate",
        help="Procesar solo un candidato específico",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        help="Modelo Gemini (default: gemini-2.5-flash)",
    )
    parser.add_argument(
        "--output-dir",
        help="Directorio de salida (default: runs/<search_id>/outputs)",
    )

    args = parser.parse_args()

    # --- Validar API Key ---
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY no configurada.")
        print("  Opciones:")
        print("  1. Crear archivo .env con GEMINI_API_KEY=tu-key")
        print("  2. export GEMINI_API_KEY=tu-key")
        print("  3. Obtener key en https://aistudio.google.com/apikey")
        sys.exit(1)

    # --- Cargar inputs ---
    if args.drive_folder:
        print("📁 Leyendo inputs desde Google Drive...")
        try:
            from agent.drive_client import DriveClient

            drive = DriveClient()
            structure = drive.discover_search_structure(args.drive_folder)
            search_inputs = structure["search_inputs"]
            candidates = structure["candidates"]
        except FileNotFoundError as e:
            print(f"❌ {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error de Drive: {e}")
            sys.exit(1)
    else:
        print(f"📁 Leyendo inputs desde: {args.local_dir}")
        if not os.path.exists(args.local_dir):
            print(f"❌ Directorio no encontrado: {args.local_dir}")
            sys.exit(1)
        search_inputs, candidates = load_local_inputs(args.local_dir)

    # --- Filtrar candidato si especificado ---
    if args.candidate:
        if args.candidate not in candidates:
            print(f"❌ Candidato '{args.candidate}' no encontrado.")
            print(f"  Candidatos disponibles: {list(candidates.keys())}")
            sys.exit(1)
        candidates = {args.candidate: candidates[args.candidate]}

    # --- Validar inputs ---
    if not search_inputs.get("jd_text"):
        print("⚠️  Advertencia: falta brief_jd.txt (input crítico para GEM5)")
    if not search_inputs.get("kickoff_notes"):
        print("⚠️  Advertencia: falta kickoff_notes.txt (input crítico para GEM5)")
    if not candidates:
        print("❌ No se encontraron candidatos. Revisar estructura de carpetas.")
        print("  Debe haber una subcarpeta por candidato con al menos cv.txt")
        sys.exit(1)

    print(f"\n  Search inputs: {list(search_inputs.keys())}")
    print(f"  Candidatos: {list(candidates.keys())}")
    for cid, cinputs in candidates.items():
        print(f"    - {cid}: {list(cinputs.keys())}")

    # --- Configurar output ---
    output_dir = args.output_dir or os.path.join("runs", args.search_id, "outputs")

    # --- Ejecutar pipeline ---
    from agent.gemini_client import GeminiClient
    from agent.pipeline import Pipeline

    gemini = GeminiClient(api_key=api_key, model=args.model)
    pipeline = Pipeline(gemini=gemini, search_id=args.search_id, output_dir=output_dir)

    results = pipeline.run_full_pipeline(search_inputs, candidates)

    # --- Resultado final ---
    summary_path = os.path.join(output_dir, "pipeline_summary.json")
    print(f"\n📄 Resumen guardado en: {summary_path}")
    print("✨ Pipeline completado.")


if __name__ == "__main__":
    main()
