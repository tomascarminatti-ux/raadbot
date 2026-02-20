import json
import os
from datetime import datetime, timezone
from typing import Optional, Any

from jsonschema import validate, ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .gemini_client import GeminiClient
from .prompt_builder import build_prompt


# Thresholds de gating
THRESHOLDS = {
    "gem1": 6,
    "gem2": 6,
    "gem3": 6,
    "gem4": 7,
}

MAX_RETRIES_ON_BLOCK = 2

# Costos Gemini 2.5 Flash (por 1M tokens)
PRICE_PROMPT_1M = 0.075
PRICE_COMPLETION_1M = 0.30

console = Console()


class Pipeline:
    """Orquestador del pipeline GEM Nivel Psicópata (Stateful & Rich UI)."""

    def __init__(self, gemini: GeminiClient, search_id: str, output_dir: str):
        self.gemini = gemini
        self.search_id = search_id
        self.output_dir = output_dir
        self.schema = self._load_schema()
        
        os.makedirs(output_dir, exist_ok=True)
        
        # State & Checkpointing
        self.state_file = os.path.join(output_dir, "pipeline_state.json")
        self.state = self._load_state()

    def _load_schema(self) -> Optional[dict]:
        schema_path = os.path.join(
            os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
        )
        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def _load_state(self) -> dict:
        """Carga el estado anterior si existe para reanudar."""
        if os.path.exists(self.state_file):
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "completed_gems": {},  # "CAND-001": ["gem1", "gem2"]
            "results_cache": {},   # Cache de outputs
            "usage": {
                "prompt_tokens": 0,
                "candidates_tokens": 0,
                "total_cost_usd": 0.0
            }
        }

    def _save_state(self):
        """Guarda el estado actual en disco."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def _track_usage(self, usage: dict):
        """Suma tokens y calcula costo acumulado."""
        if not usage:
            return
        
        p_tokens = usage.get("prompt_tokens", 0)
        c_tokens = usage.get("candidates_tokens", 0)
        
        self.state["usage"]["prompt_tokens"] += p_tokens
        self.state["usage"]["candidates_tokens"] += c_tokens
        
        cost_p = (p_tokens / 1_000_000) * PRICE_PROMPT_1M
        cost_c = (c_tokens / 1_000_000) * PRICE_COMPLETION_1M
        self.state["usage"]["total_cost_usd"] += (cost_p + cost_c)
        
        self._save_state()

    def _save_output(self, gem_name: str, result: dict, candidate_id: Optional[str] = None):
        """Guarda output JSON y Markdown y trackea estado."""
        prefix = gem_name
        if candidate_id:
            candidate_dir = os.path.join(self.output_dir, candidate_id)
            os.makedirs(candidate_dir, exist_ok=True)
            base = candidate_dir
            state_key = candidate_id
        else:
            base = self.output_dir
            state_key = "search"

        # Track usage
        if "usage" in result:
            self._track_usage(result["usage"])

        # Update state cache
        if state_key not in self.state["completed_gems"]:
            self.state["completed_gems"][state_key] = []
        if gem_name not in self.state["completed_gems"][state_key]:
            self.state["completed_gems"][state_key].append(gem_name)
        
        if state_key not in self.state["results_cache"]:
            self.state["results_cache"][state_key] = {}
        self.state["results_cache"][state_key][gem_name] = result
        self._save_state()

        # Files
        json_path = os.path.join(base, f"{prefix}.json")
        if result.get("json"):
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result["json"], f, ensure_ascii=False, indent=2)

        md_path = os.path.join(base, f"{prefix}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(result.get("markdown", result.get("raw", "")))

        raw_path = os.path.join(base, f"{prefix}.raw.txt")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(result.get("raw", ""))

        return json_path, md_path

    def _validate_output(self, json_data: dict, gem_name: str) -> bool:
        if not self.schema or not json_data:
            return True
        try:
            validate(instance=json_data, schema=self.schema)
            return True
        except ValidationError as e:
            console.print(f"[bold yellow]  ⚠️  Schema validation warning ({gem_name}):[/bold yellow] {e.message}")
            return False

    def _get_score(self, json_data: dict) -> Optional[int]:
        if not json_data:
            return None
        scores = json_data.get("scores", {})
        return scores.get("score_dimension")

    def _check_gate(self, gem_name: str, score: Optional[int]) -> bool:
        threshold = THRESHOLDS.get(gem_name)
        if threshold is None or score is None:
            return True
        return score >= threshold

    def run_gem5(self, search_inputs: dict) -> dict:
        console.print(Panel(f"[bold cyan]🔍 Ejecutando GEM5 – Radiografía Estratégica[/bold cyan]\nSearch ID: {self.search_id}", border_style="cyan"))

        # Skip if cached
        if "gem5" in self.state["completed_gems"].get("search", []):
            console.print("[dim]  ⏭️  GEM5 completado previamente. Recuperando de caché...[/dim]")
            return self.state["results_cache"]["search"]["gem5"]

        variables = {
            "search_id": self.search_id,
            **search_inputs,
        }

        with console.status("[cyan]Analizando rol y compañía con IA...[/cyan]", spinner="dots"):
            prompt = build_prompt("gem5", variables)
            result = self.gemini.run_gem(prompt)

        self._save_output("gem5", result)
        self._validate_output(result.get("json"), "gem5")

        confidence = (result.get("json") or {}).get("scores", {}).get("confidence")
        console.print(f"[bold green]  ✅ GEM5 completado[/bold green] | Confidence: {confidence}")

        return result

    def run_candidate_pipeline(
        self,
        candidate_id: str,
        candidate_inputs: dict,
        gem5_result: dict,
    ) -> dict:
        console.print(Panel(f"[bold magenta]👤 Procesando Candidato: {candidate_id}[/bold magenta]", border_style="magenta"))

        results: dict[str, Any] = {"candidate_id": candidate_id, "gems": {}}
        gem5_json = gem5_result.get("json", {})
        gem5_content = gem5_json.get("content", {}) if gem5_json else {}
        
        completed = self.state["completed_gems"].get(candidate_id, [])
        cache = self.state["results_cache"].get(candidate_id, {})

        # --- GEM1: Trayectoria y Logros ---
        console.print("\n[bold]📋 GEM1 – Trayectoria y Logros[/bold]")
        if "gem1" in completed:
            console.print("[dim]  ⏭️  Recuperando de caché...[/dim]")
            gem1_result = cache["gem1"]
        else:
            gem1_vars = {
                "search_id": self.search_id,
                "candidate_id": candidate_id,
                "cv_text": candidate_inputs.get("cv_text", "No proporcionado"),
                "interview_notes": candidate_inputs.get("interview_notes", "No proporcionado"),
                "gem5_summary": json.dumps(gem5_content, ensure_ascii=False) if gem5_content else gem5_result.get("markdown", ""),
            }

            with console.status("[blue]Extrayendo trayectoria...[/blue]"):
                gem1_prompt = build_prompt("gem1", gem1_vars)
                gem1_result = self.gemini.run_gem(gem1_prompt)
                self._save_output("gem1", gem1_result, candidate_id)
        
        results["gems"]["gem1"] = gem1_result
        gem1_score = self._get_score(gem1_result.get("json"))
        
        if not self._check_gate("gem1", gem1_score):
            console.print(f"[bold red]  ❌ GEM1 score ({gem1_score}) < 6. Candidato descartado.[/bold red]")
            results["decision"] = "DESCARTADO_GEM1"
            return results
        console.print(f"[green]  ✅ GEM1 aprobado[/green] (score {gem1_score} ≥ 6)")

        # --- GEM2: Assessment a Negocio ---
        console.print("\n[bold]🧠 GEM2 – Assessment a Negocio[/bold]")
        if "gem2" in completed:
            console.print("[dim]  ⏭️  Recuperando de caché...[/dim]")
            gem2_result = cache["gem2"]
        else:
            gem2_vars = {
                "search_id": self.search_id,
                "candidate_id": candidate_id,
                "gem1": gem1_result.get("json") or gem1_result.get("raw", ""),
                "tests_text": candidate_inputs.get("tests_text", "No proporcionado"),
                "case_notes": candidate_inputs.get("case_notes", "No proporcionado"),
                "gem5_key_challenge": gem5_content.get("problema_real_del_rol", gem5_result.get("markdown", "No disponible")),
            }

            with console.status("[blue]Realizando assessment contra contexto de compañía...[/blue]"):
                gem2_prompt = build_prompt("gem2", gem2_vars)
                gem2_result = self.gemini.run_gem(gem2_prompt)
                self._save_output("gem2", gem2_result, candidate_id)
                
        results["gems"]["gem2"] = gem2_result
        gem2_score = self._get_score(gem2_result.get("json"))

        if not self._check_gate("gem2", gem2_score):
            console.print(f"[bold red]  ❌ GEM2 score ({gem2_score}) < 6. Candidato descartado.[/bold red]")
            results["decision"] = "DESCARTADO_GEM2"
            return results
        console.print(f"[green]  ✅ GEM2 aprobado[/green] (score {gem2_score} ≥ 6)")

        # --- GEM3: Veredicto + Referencias 360° ---
        console.print("\n[bold]🔎 GEM3 – Veredicto + Referencias 360°[/bold]")
        if "gem3" in completed:
            console.print("[dim]  ⏭️  Recuperando de caché...[/dim]")
            gem3_result = cache["gem3"]
        else:
            gem3_vars = {
                "search_id": self.search_id,
                "candidate_id": candidate_id,
                "gem1": gem1_result.get("json") or gem1_result.get("raw", ""),
                "gem2": gem2_result.get("json") or gem2_result.get("raw", ""),
                "references_text": candidate_inputs.get("references_text", "No proporcionado"),
                "client_culture": candidate_inputs.get("client_culture", "No proporcionado"),
            }

            with console.status("[blue]Cruzando datos y referencias...[/blue]"):
                gem3_prompt = build_prompt("gem3", gem3_vars)
                gem3_result = self.gemini.run_gem(gem3_prompt)
                self._save_output("gem3", gem3_result, candidate_id)
                
        results["gems"]["gem3"] = gem3_result
        gem3_score = self._get_score(gem3_result.get("json"))

        if not self._check_gate("gem3", gem3_score):
            console.print(f"[bold red]  ❌ GEM3 score ({gem3_score}) < 6. Candidato descartado.[/bold red]")
            results["decision"] = "DESCARTADO_GEM3"
            return results
        console.print(f"[green]  ✅ GEM3 aprobado[/green] (score {gem3_score} ≥ 6)")

        # --- GEM4: Auditor QA ---
        console.print("\n[bold]🛡️  GEM4 – Auditor QA (Gate Final)[/bold]")
        
        if "gem4" in completed:
            console.print("[dim]  ⏭️  Recuperando de caché...[/dim]")
            gem4_result = cache["gem4"]
        else:
            sources = []
            for key in ["cv_text", "interview_notes", "tests_text", "case_notes", "references_text"]:
                if candidate_inputs.get(key) and candidate_inputs[key] != "No proporcionado":
                    sources.append(key)

            with console.status("[yellow]Ejecutando auditoría QA rigurosa...[/yellow]"):
                gem4_result = self._run_gem4_with_retries(candidate_id, gem1_result, gem2_result, gem3_result, sources)
                
        results["gems"]["gem4"] = gem4_result

        gem4_json = gem4_result.get("json", {})
        decision = (gem4_json or {}).get("decision", "DESCONOCIDO")
        gem4_score = self._get_score(gem4_json)

        results["decision"] = decision
        results["gem4_score"] = gem4_score

        if decision == "APROBADO":
            console.print(f"\n[bold green]  🎉 REPORTE APROBADO[/bold green] (QA score: {gem4_score})")
        else:
            console.print(f"\n[bold red]  🚫 REPORTE BLOQUEADO[/bold red] (QA score: {gem4_score}) - Escalando a consultor.")

        return results

    def _run_gem4_with_retries(self, candidate_id: str, gem1_result: dict, gem2_result: dict, gem3_result: dict, sources: list, attempt: int = 0) -> dict:
        gem4_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "gem1": gem1_result.get("json") or gem1_result.get("raw", ""),
            "gem2": gem2_result.get("json") or gem2_result.get("raw", ""),
            "gem3": gem3_result.get("json") or gem3_result.get("raw", ""),
            "sources_index": ", ".join(sources),
        }

        gem4_prompt = build_prompt("gem4", gem4_vars)
        gem4_result = self.gemini.run_gem(gem4_prompt)
        
        # Guardaremos los intentos fallidos con sufijos si es necesario, 
        # pero para mantener simple, pisamos o guardamos el ultimo.
        self._save_output("gem4", gem4_result, candidate_id)

        gem4_json = gem4_result.get("json", {})
        gem4_score = self._get_score(gem4_json)
        decision = (gem4_json or {}).get("decision", "BLOQUEADO")

        console.print(f"  Score QA: {gem4_score} | Decisión: {decision}")

        if decision != "BLOQUEADO" and self._check_gate("gem4", gem4_score):
            return gem4_result

        if attempt < MAX_RETRIES_ON_BLOCK:
            console.print(f"[bold yellow]  🔄 Intento {attempt + 1}/{MAX_RETRIES_ON_BLOCK} de corrección automática...[/bold yellow]")
            return self._run_gem4_with_retries(candidate_id, gem1_result, gem2_result, gem3_result, sources, attempt + 1)

        console.print("[bold red]  ⛔ Máximo de reintentos QA alcanzado.[/bold red]")
        return gem4_result

    def run_full_pipeline(self, search_inputs: dict, candidates: dict[str, dict]) -> dict:
        timestamp = datetime.now(timezone.utc).isoformat()
        
        console.rule(f"[bold gold1]RAADBot Pipeline Runner v1.4 – {self.search_id}[/bold gold1]")
        console.print(f"[dim]Timestamp: {timestamp} | Candidatos en cola: {len(candidates)}[/dim]\n")

        # 1. GEM5
        gem5_result = self.run_gem5(search_inputs)

        all_results = {
            "search_id": self.search_id,
            "timestamp": timestamp,
            "gem5": gem5_result,
            "candidates": {},
        }

        # 2. Iterar candidatos
        for candidate_id, candidate_inputs in candidates.items():
            try:
                result = self.run_candidate_pipeline(candidate_id, candidate_inputs, gem5_result)
                all_results["candidates"][candidate_id] = result
            except Exception as e:
                console.print(f"[bold red]❌ Error crítico procesando candidato {candidate_id}: {e}[/bold red]")
                all_results["candidates"][candidate_id] = {
                    "candidate_id": candidate_id,
                    "decision": f"ERROR_EJECUCION: {e}",
                    "gem4_score": None,
                }

        # 3. Guardar resumen JSON final
        summary_path = os.path.join(self.output_dir, "pipeline_summary.json")
        summary = {
            "search_id": self.search_id,
            "timestamp": timestamp,
            "candidates": {
                cid: {
                    "decision": r.get("decision"),
                    "gem4_score": r.get("gem4_score"),
                }
                for cid, r in all_results["candidates"].items()
            },
        }
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        # 4. Imprimir Tabla Final Resumen Nivel Psicopata
        self._print_summary(all_results)
        
        return all_results

    def _print_summary(self, results: dict):
        console.print("\n")
        
        # Tabla de Candidatos
        table = Table(title="💎 Dashboard Final de Decisión", show_header=True, header_style="bold magenta")
        table.add_column("Candidato", style="dim", width=15)
        table.add_column("Decisión Final", justify="center")
        table.add_column("Score QA")
        table.add_column("Status")

        for cid, cresult in results["candidates"].items():
            decision = cresult.get("decision", "?")
            score = str(cresult.get("gem4_score", "?"))
            
            if decision == "APROBADO":
                status = "[green]Ready for Client[/green]"
                icon = "✅"
            elif "DESCARTADO" in decision:
                status = f"[red]Rechazado en {decision.split('_')[-1]}[/red]"
                icon = "❌"
            elif "ERROR" in decision:
                status = "[bold red]Crash[/bold red]"
                icon = "⚠️"
            else:
                status = "[yellow]Escalado (Requires Review)[/yellow]"
                icon = "🚫"
                
            table.add_row(cid, f"{icon} {decision}", score, status)

        console.print(table)
        
        # Panel de Costos USD
        usage = self.state.get("usage", {})
        cost = usage.get("total_cost_usd", 0.0)
        p_tok = usage.get("prompt_tokens", 0)
        c_tok = usage.get("candidates_tokens", 0)
        
        cost_panel = Panel(
            f"💰 Costo total estimado: [bold green]${cost:.4f} USD[/bold green]\n"
            f"📊 Prompt Tokens: {p_tok:,} | Completion Tokens: {c_tok:,}",
            title="Consumo de API",
            border_style="green"
        )
        console.print(cost_panel)
