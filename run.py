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
import asyncio

from dotenv import load_dotenv

from agent.utils import load_local_inputs
from agent.config import DEFAULT_MODEL


async def run_pipeline_async():
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
        default=DEFAULT_MODEL,
        help=f"Modelo Gemini (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--output-dir",
        help="Directorio de salida (default: runs/<search_id>/outputs)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Habilita la salida estricta en JSON para integraciones como n8n",
    )

    args = parser.parse_args()

    # --- Support para JSON CLI Mode ---
    original_stdout = sys.stdout
    if args.json:
        sys.stdout = open(os.devnull, "w")

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
        try:
            search_inputs, candidates = load_local_inputs(args.local_dir)
        except Exception as e:
            print(f"❌ Error cargando inputs locales: {e}")
            sys.exit(1)

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

    results = await pipeline.run_full_pipeline(search_inputs, candidates)

    # --- Resultado final ---
    summary_path = os.path.join(output_dir, "pipeline_summary.json")

    if args.json:
        sys.stdout = original_stdout
        if os.path.exists(summary_path):
            with open(summary_path, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print(
                json.dumps(
                    {
                        "error": "Pipeline failed or no summary generated",
                        "status": "error",
                    }
                )
            )
    else:
        print(f"\n📄 Resumen guardado en: {summary_path}")
        print("✨ Pipeline completado.")


if __name__ == "__main__":
    asyncio.run(run_pipeline_async())
