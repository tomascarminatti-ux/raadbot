#!/usr/bin/env python3
"""
run.py – Entry point para el pipeline RAAD GEM.

Uso:
    # Con Google Drive
    python run.py --search-id SEARCH-2026-001 --drive-folder <FOLDER_ID>

    # Con carpeta local
    python run.py --search-id SEARCH-2026-001 --local-dir ./inputs

    # Solo un candidato
    python run.py --search-id SEARCH-2026-001 --local-dir ./inputs --candidate CAND-001
"""

import argparse
import json
import os
import sys
from rich.console import Console

import config
from utils.input_loader import load_local_inputs
from agent.gemini_client import GeminiClient
from agent.pipeline import Pipeline
from agent.drive_client import DriveClient

console = Console()

def main():
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
        default=config.DEFAULT_MODEL,
        help=f"Modelo Gemini (default: {config.DEFAULT_MODEL})",
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

    # --- CLI Support ---
    if args.json:
        # Disable rich output for JSON mode
        import io
        from rich.console import Console as RichConsole
        non_rich_console = RichConsole(file=io.StringIO())
        # Global console override would be better but this is a quick fix
    
    # --- API Key check ---
    api_key = config.GEMINI_API_KEY
    if not api_key:
        console.print("[bold red]❌ Error: GEMINI_API_KEY no configurada.[/bold red]")
        console.print("  Por favor configura tu API key en el archivo [bold].env[/bold]")
        sys.exit(1)

    # --- Load inputs ---
    search_inputs = {}
    candidates = {}

    if args.drive_folder:
        console.print(f"📁 [cyan]Leyendo inputs desde Google Drive...[/cyan]")
        try:
            drive = DriveClient(credentials_path=config.DRIVE_CREDENTIALS_PATH)
            structure = drive.discover_search_structure(args.drive_folder)
            search_inputs = structure["search_inputs"]
            candidates = structure["candidates"]
        except Exception as e:
            console.print(f"[bold red]❌ Error de Drive: {e}[/bold red]")
            sys.exit(1)
    else:
        console.print(f"📁 [cyan]Leyendo inputs desde: {args.local_dir}[/cyan]")
        if not os.path.exists(args.local_dir):
            console.print(f"[bold red]❌ Directorio no encontrado: {args.local_dir}[/bold red]")
            sys.exit(1)
        search_inputs, candidates = load_local_inputs(args.local_dir)

    # --- Filter candidate ---
    if args.candidate:
        if args.candidate not in candidates:
            console.print(f"[bold red]❌ Candidato '{args.candidate}' no encontrado.[/bold red]")
            console.print(f"  Candidatos disponibles: {list(candidates.keys())}")
            sys.exit(1)
        candidates = {args.candidate: candidates[args.candidate]}

    # --- Validation ---
    if not search_inputs.get("jd_text"):
        console.print("[yellow]⚠️  Advertencia: falta brief_jd.txt (input crítico para GEM5)[/yellow]")
    if not candidates:
        console.print("[bold red]❌ No se encontraron candidatos. Revisar estructura de carpetas.[/bold red]")
        sys.exit(1)

    # --- Output configuration ---
    output_dir = args.output_dir or os.path.join("runs", args.search_id, "outputs")

    # --- Run Pipeline ---
    gemini = GeminiClient(api_key=api_key, model=args.model)
    pipeline = Pipeline(gemini=gemini, search_id=args.search_id, output_dir=output_dir)

    results = pipeline.run_full_pipeline(search_inputs, candidates)

    # --- Final result ---
    summary_path = os.path.join(output_dir, "pipeline_summary.json")

    if args.json:
        if os.path.exists(summary_path):
            with open(summary_path, "r", encoding="utf-8") as f:
                # Use print directly to ensure clean JSON stdout
                sys.stdout.write(f.read() + "\n")
        else:
            sys.stdout.write(json.dumps({"error": "No summary generated", "status": "error"}) + "\n")
    else:
        console.print(f"\n📄 Resumen guardado en: [bold]{summary_path}[/bold]")
        console.print("[bold green]✨ Pipeline completado.[/bold green]")


if __name__ == "__main__":
    main()
