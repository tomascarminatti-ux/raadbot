import json
import os
import time
from datetime import datetime, timezone
from typing import Optional, Any, Tuple, Dict, List

from jsonschema import validate, ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import config
from agent.gemini_client import GeminiClient, GeminiResult
from agent.prompt_builder import build_prompt

console = Console()

class Pipeline:
    """
    Orquestador del pipeline GEM Nivel Psicópata (Stateful & Rich UI).
    Maneja la ejecución secuencial de GEMs, validación de schemas y checkpointing.
    """

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
        """Carga el schema de validación JSON."""
        schema_path = os.path.join(
            os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
        )
        if os.path.exists(schema_path):
            try:
                with open(schema_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                console.print(f"[bold red]  ❌ Error cargando schema ({e}). Validaciones desactivadas.[/bold red]")
        return None

    def _load_state(self) -> dict:
        """Carga el estado anterior si existe para reanudar la ejecución."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                console.print(f"[bold yellow]  ⚠️  Error cargando estado ({e}). Reseteando...[/bold yellow]")
        return {
            "completed_gems": {},  # "CAND-001": ["gem1", "gem2"]
            "results_cache": {},  # Cache de outputs
            "usage": {
                "prompt_tokens": 0,
                "candidates_tokens": 0,
                "total_cost_usd": 0.0,
            },
        }

    def _save_state(self):
        """Guarda el estado actual en disco."""
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            console.print(f"[bold red]  ⚠️  No se pudo guardar el estado: {e}[/bold red]")

    def _track_usage(self, usage: Dict[str, Any]):
        """Suma tokens y calcula costo acumulado basado en config.PRICE_*."""
        if not usage:
            return

        p_tokens = usage.get("prompt_tokens", 0)
        c_tokens = usage.get("candidates_tokens", 0)

        self.state["usage"]["prompt_tokens"] += p_tokens
        self.state["usage"]["candidates_tokens"] += c_tokens

        cost_p = (p_tokens / 1_000_000) * config.PRICE_PROMPT_1M
        cost_c = (c_tokens / 1_000_000) * config.PRICE_COMPLETION_1M
        self.state["usage"]["total_cost_usd"] += cost_p + cost_c

        self._save_state()

    def _save_output(
        self, gem_name: str, result: GeminiResult, candidate_id: Optional[str] = None
    ) -> Tuple[str, str]:
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
        
        # Guardar en caché el resultado (excluyendo el raw si es muy pesado, opcionalmente)
        self.state["results_cache"][state_key][gem_name] = result
        self._save_state()

        # Files
        json_path = os.path.join(base, f"{prefix}.json")
        if result.get("json"):
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result["json"], f, ensure_ascii=False, indent=2)

        md_path = os.path.join(base, f"{prefix}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            md_content = result.get("markdown")
            if md_content is None:
                md_content = result.get("raw", "")
            f.write(str(md_content))

        raw_path = os.path.join(base, f"{prefix}.raw.txt")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(result.get("raw", ""))

        return json_path, md_path

    def _normalize_gem_name(self, name: str) -> str:
        """Normaliza nombres como GEM1, GEM_1, gem_1 a gem1."""
        return name.lower().replace("_", "").replace("-", "")

    def _validate_output(self, json_data: Optional[Dict[str, Any]], gem_name: str) -> bool:
        """Valida que el JSON generado cumpla con el schema."""
        if not json_data:
            raise ValueError(f"Output nulo o sin JSON válido en {gem_name}")
            
        if not self.schema:
            return True # No hay schema cargado, saltar validación formal

        # Validación lógica: ¿Corresponde el JSON al GEM esperado?
        meta = json_data.get("meta", {})
        json_gem = meta.get("gem")
        if json_gem:
            if self._normalize_gem_name(str(json_gem)) != self._normalize_gem_name(gem_name):
                console.print(f"[dim]    ℹ️  GEM Name Mismatch: Prompt reportó {json_gem}, esperado {gem_name}[/dim]")

        try:
            validate(instance=json_data, schema=self.schema)
            return True
        except ValidationError as e:
            raise ValueError(f"Schema fallido en {gem_name}: {e.message}")

    def _get_score(self, json_data: Optional[Dict[str, Any]]) -> Optional[int]:
        """Extrae el score de negocio del JSON."""
        if not json_data:
            return None
        scores = json_data.get("scores", {})
        return scores.get("score_dimension")

    def _check_gate(self, gem_name: str, score: Optional[int]) -> bool:
        """Verifica si un score cumple el umbral definido en config."""
        threshold = config.THRESHOLDS.get(gem_name)
        if threshold is None:
            return True # No hay umbral, siempre pasa
        if score is None:
            return False
        return score >= threshold

    def _run_gem_with_validation(self, gem_name: str, prompt_vars: dict) -> GeminiResult:
        """Ejecuta un GEM con reintentos si la validación falla."""
        for attempt in range(config.MAX_RETRIES_ON_BLOCK + 1):
            prompt = build_prompt(gem_name, prompt_vars)
            result = self.gemini.run_gem(prompt)

            try:
                self._validate_output(result.get("json"), gem_name)
                return result
            except ValueError as e:
                if attempt < config.MAX_RETRIES_ON_BLOCK:
                    console.print(
                        f"[bold yellow]  ⚠️  Error de validación ({e}). Reintentando {attempt+1}/{config.MAX_RETRIES_ON_BLOCK}...[/bold yellow]"
                    )
                    time.sleep(2)
                else:
                    console.print(
                        f"[bold red]  ❌ Error definitivo de validación en {gem_name}.[/bold red]"
                    )
                    return result
        return {"json": None, "markdown": "", "raw": "", "usage": {}}  # Fallback final

    def _run_generic_gem_step(
        self, gem_name: str, candidate_id: str, prompt_vars: dict, display_name: str
    ) -> Tuple[GeminiResult, Optional[int], bool]:
        """Paso genérico que envuelve la ejecución, guardado y chequeo de gate."""
        console.print(f"\n[bold]📋 {display_name}[/bold]")
        cache = self.state["results_cache"].get(candidate_id, {})

        if gem_name in self.state["completed_gems"].get(candidate_id, []):
            console.print("[dim]  ⏭️  Recuperando de caché...[/dim]")
            result = cache[gem_name]
        else:
            with console.status(f"[blue]Ejecutando {gem_name}...[/blue]"):
                result = self._run_gem_with_validation(gem_name, prompt_vars)
                self._save_output(gem_name, result, candidate_id)

        score = self._get_score(result.get("json"))

        if score is None:
            console.print(
                f"[bold red]  ❌ Error parseando score en {gem_name}. Fallo automático.[/bold red]"
            )
            return result, score, False

        passed = self._check_gate(gem_name, score)
        if not passed:
            console.print(
                f"[bold red]  ❌ {gem_name} score ({score}) < {config.THRESHOLDS.get(gem_name)}. Candidato descartado.[/bold red]"
            )
        else:
            console.print(f"[green]  ✅ {gem_name} aprobado[/green] (score {score})")

        return result, score, passed

    def run_gem5(self, search_inputs: dict) -> GeminiResult:
        """Ejecuta GEM5 (Radiografía Estratégica)."""
        console.print(
            Panel(
                f"[bold cyan]🔍 Ejecutando GEM5 – Radiografía Estratégica[/bold cyan]\nSearch ID: {self.search_id}",
                border_style="cyan",
            )
        )

        if "gem5" in self.state["completed_gems"].get("search", []):
            console.print(
                "[dim]  ⏭️  GEM5 completado previamente. Recuperando de caché...[/dim]"
            )
            return self.state["results_cache"]["search"]["gem5"]

        variables = {
            "search_id": self.search_id,
            **search_inputs,
        }

        with console.status(
            "[cyan]Analizando rol y compañía con IA...[/cyan]", spinner="dots"
        ):
            result = self._run_gem_with_validation("gem5", variables)

        self._save_output("gem5", result)
        confidence = (result.get("json") or {}).get("scores", {}).get("confidence")
        console.print(
            f"[bold green]  ✅ GEM5 completado[/bold green] | Confidence: {confidence}"
        )

        return result

    def run_candidate_pipeline(
        self,
        candidate_id: str,
        candidate_inputs: dict,
        gem5_result: GeminiResult,
    ) -> dict:
        """Ejecuta secuencialmente GEM1, GEM2, GEM3 y GEM4 para un candidato."""
        console.print(
            Panel(
                f"[bold magenta]👤 Procesando Candidato: {candidate_id}[/bold magenta]",
                border_style="magenta",
            )
        )

        results: dict[str, Any] = {"candidate_id": candidate_id, "gems": {}}
        gem5_json = gem5_result.get("json", {})
        gem5_content = gem5_json.get("content", {}) if gem5_json else {}

        # Preparar resúmenes de GEM5 para los siguientes prompts
        gem5_summary = (
            json.dumps(gem5_content, ensure_ascii=False)
            if gem5_content
            else gem5_result.get("markdown", "")
        )
        gem5_key_challenge = gem5_content.get(
            "problema_real_del_rol", gem5_result.get("markdown", "No disponible")
        )

        # --- GEM1: Trayectoria ---
        gem1_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "cv_text": candidate_inputs.get("cv_text", "No proporcionado"),
            "interview_notes": candidate_inputs.get(
                "interview_notes", "No proporcionado"
            ),
            "gem5_summary": gem5_summary,
        }
        gem1_result, gem1_score, passed1 = self._run_generic_gem_step(
            "gem1", candidate_id, gem1_vars, "GEM1 – Trayectoria y Logros"
        )
        results["gems"]["gem1"] = gem1_result
        if not passed1:
            results["decision"] = "DESCARTADO_GEM1"
            return results

        # --- GEM2: Assessment Negocio ---
        gem2_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "gem1": gem1_result.get("json") or gem1_result.get("raw", ""),
            "tests_text": candidate_inputs.get("tests_text", "No proporcionado"),
            "case_notes": candidate_inputs.get("case_notes", "No proporcionado"),
            "gem5_key_challenge": gem5_key_challenge,
        }
        gem2_result, gem2_score, passed2 = self._run_generic_gem_step(
            "gem2", candidate_id, gem2_vars, "GEM2 – Assessment a Negocio"
        )
        results["gems"]["gem2"] = gem2_result
        if not passed2:
            results["decision"] = "DESCARTADO_GEM2"
            return results

        # --- GEM3: Veredicto 360 ---
        gem3_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "gem1": gem1_result.get("json") or gem1_result.get("raw", ""),
            "gem2": gem2_result.get("json") or gem2_result.get("raw", ""),
            "references_text": candidate_inputs.get(
                "references_text", "No proporcionado"
            ),
            "client_culture": candidate_inputs.get(
                "client_culture", "No proporcionado"
            ),
        }
        gem3_result, gem3_score, passed3 = self._run_generic_gem_step(
            "gem3", candidate_id, gem3_vars, "GEM3 – Veredicto + Referencias 360°"
        )
        results["gems"]["gem3"] = gem3_result
        if not passed3:
            results["decision"] = "DESCARTADO_GEM3"
            return results

        # --- GEM4: Auditor QA ---
        sources = [k for k in ["cv_text", "interview_notes", "tests_text", "case_notes", "references_text"] 
                   if candidate_inputs.get(k) and candidate_inputs[k] != "No proporcionado"]

        gem4_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "gem1": gem1_result.get("json") or gem1_result.get("raw", ""),
            "gem2": gem2_result.get("json") or gem2_result.get("raw", ""),
            "gem3": gem3_result.get("json") or gem3_result.get("raw", ""),
            "sources_index": ", ".join(sources),
        }
        gem4_result, gem4_score, passed4 = self._run_generic_gem_step(
            "gem4", candidate_id, gem4_vars, "GEM4 – Auditor QA (Gate Final)"
        )
        results["gems"]["gem4"] = gem4_result

        gem4_json = gem4_result.get("json", {})
        decision = (gem4_json or {}).get("decision", "BLOQUEADO")

        if gem4_score is not None and passed4 and decision != "BLOQUEADO":
            decision = "APROBADO"

        results["decision"] = decision
        results["gem4_score"] = gem4_score

        if decision == "APROBADO":
            console.print(
                f"\n[bold green]  🎉 REPORTE APROBADO[/bold green] (QA score: {gem4_score})"
            )
        else:
            console.print(
                f"\n[bold red]  🚫 REPORTE BLOQUEADO[/bold red] (QA score: {gem4_score}) - Escalando a consultor."
            )

        return results

    def run_full_pipeline(
        self, search_inputs: dict, candidates: dict[str, dict]
    ) -> dict:
        """Ejecución maestra del pipeline para todos los candidatos."""
        timestamp = datetime.now(timezone.utc).isoformat()

        console.rule(
            f"[bold gold1]RAADBot Pipeline Runner v1.5 – {self.search_id}[/bold gold1]"
        )
        console.print(
            f"[dim]Timestamp: {timestamp} | Candidatos en cola: {len(candidates)}[/dim]\n"
        )

        # 1. GEM5 (Contexto búsqueda)
        gem5_result = self.run_gem5(search_inputs)

        all_results: dict[str, Any] = {
            "search_id": self.search_id,
            "timestamp": timestamp,
            "gem5": gem5_result,
            "candidates": {},
        }

        # 2. Iterar candidatos
        for candidate_id, candidate_inputs in candidates.items():
            try:
                result = self.run_candidate_pipeline(
                    candidate_id, candidate_inputs, gem5_result
                )
                all_results["candidates"][candidate_id] = result
            except Exception as e:
                console.print(
                    f"[bold red]❌ Error crítico procesando candidato {candidate_id}: {e}[/bold red]"
                )
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

        # 4. Dashboard final
        self._print_summary(all_results)

        return all_results

    def _print_summary(self, results: dict):
        """Imprime tabla resumen de resultados y costos."""
        console.print("\n")

        table = Table(
            title="💎 Dashboard Final de Decisión",
            show_header=True,
            header_style="bold magenta",
        )
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

        usage = self.state.get("usage", {})
        cost = usage.get("total_cost_usd", 0.0)
        p_tok = usage.get("prompt_tokens", 0)
        c_tok = usage.get("candidates_tokens", 0)

        cost_panel = Panel(
            f"💰 Costo total estimado: [bold green]${cost:.4f} USD[/bold green]\n"
            f"📊 Prompt Tokens: {p_tok:,} | Completion Tokens: {c_tok:,}",
            title="Consumo de API",
            border_style="green",
        )
        console.print(cost_panel)
