import json
import os
import asyncio
from datetime import datetime, timezone
from typing import Optional, Any

from jsonschema import validate, ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent.gemini_client import GeminiClient
from agent.prompt_builder import build_prompt
from agent.config import THRESHOLDS, MAX_RETRIES_ON_BLOCK, PRICE_PROMPT_1M, PRICE_COMPLETION_1M
from agent.logger import logger


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
        self._lock = asyncio.Lock()

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
            "results_cache": {},  # Cache de outputs
            "usage": {
                "prompt_tokens": 0,
                "candidates_tokens": 0,
                "total_cost_usd": 0.0,
            },
        }

    async def _save_state(self):
        """Guarda el estado actual en disco (con lock para concurrencia)."""
        async with self._lock:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)

    async def _track_usage(self, usage: dict):
        """Suma tokens y calcula costo acumulado."""
        if not usage:
            return

        p_tokens = usage.get("prompt_tokens", 0)
        c_tokens = usage.get("candidates_tokens", 0)

        async with self._lock:
            self.state["usage"]["prompt_tokens"] += p_tokens
            self.state["usage"]["candidates_tokens"] += c_tokens

            cost_p = (p_tokens / 1_000_000) * PRICE_PROMPT_1M
            cost_c = (c_tokens / 1_000_000) * PRICE_COMPLETION_1M
            self.state["usage"]["total_cost_usd"] += cost_p + cost_c

        await self._save_state()

    async def _save_output(
        self, gem_name: str, result: dict, candidate_id: Optional[str] = None
    ):
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
            await self._track_usage(result["usage"])

        async with self._lock:
            # Update state cache
            if state_key not in self.state["completed_gems"]:
                self.state["completed_gems"][state_key] = []
            if gem_name not in self.state["completed_gems"][state_key]:
                self.state["completed_gems"][state_key].append(gem_name)

            if state_key not in self.state["results_cache"]:
                self.state["results_cache"][state_key] = {}
            self.state["results_cache"][state_key][gem_name] = result

        await self._save_state()

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

    def _validate_output(self, json_data: dict, gem_name: str) -> bool:
        if not self.schema or not json_data:
            raise ValueError(f"Output nulo o sin JSON válido en {gem_name}")
        try:
            validate(instance=json_data, schema=self.schema)
            return True
        except ValidationError as e:
            raise ValueError(f"Schema fallido en {gem_name}: {e.message}")

    def _get_score(self, json_data: Optional[dict]) -> Optional[int]:
        if not json_data:
            return None
        scores = json_data.get("scores", {})
        return scores.get("score_dimension")

    def _check_gate(self, gem_name: str, score: Optional[int]) -> bool:
        threshold = THRESHOLDS.get(gem_name)
        if threshold is None:
            return True
        if score is None:
            return False
        return score >= threshold

    async def _run_gem_with_validation(self, gem_name: str, prompt_vars: dict) -> dict:
        for attempt in range(MAX_RETRIES_ON_BLOCK + 1):
            prompt = build_prompt(gem_name, prompt_vars)
            result = await self.gemini.run_gem_async(prompt)

            try:
                self._validate_output(result.get("json"), gem_name)
                return result
            except ValueError as e:
                if attempt < MAX_RETRIES_ON_BLOCK:
                    logger.warning(f"⚠️ Error de validación en {gem_name} ({e}). Reintentando {attempt+1}/{MAX_RETRIES_ON_BLOCK}...")
                    await asyncio.sleep(2)
                else:
                    logger.error(f"❌ Error definitivo de validación en {gem_name}.")
                    return result
        return {}  # Fallback final para el linter

    async def _run_generic_gem_step(
        self, gem_name: str, candidate_id: str, prompt_vars: dict, display_name: str
    ) -> Any:
        # console.print(f"\n[bold]📋 {display_name}[/bold]") # Deshabilitado en paralelo para evitar ruido

        async with self._lock:
            cache = self.state["results_cache"].get(candidate_id, {})
            completed = gem_name in self.state["completed_gems"].get(candidate_id, [])

        if completed:
            # console.print("[dim]  ⏭️  Recuperando de caché...[/dim]")
            result = cache[gem_name]
        else:
            # with console.status(f"[blue]Ejecutando {gem_name}...[/blue]"):
            result = await self._run_gem_with_validation(gem_name, prompt_vars)
            await self._save_output(gem_name, result, candidate_id)

        score = self._get_score(result.get("json"))

        if score is None:
            logger.error(f"❌ Error parseando score en {gem_name} para {candidate_id}. Fallo automático.")
            return result, score, False

        passed = self._check_gate(gem_name, score)
        if not passed:
            logger.warning(f"⚠️ {gem_name} score ({score}) < {THRESHOLDS.get(gem_name)} para {candidate_id}. Candidato descartado en este punto.")
        else:
            pass # console.print(f"[green]  ✅ {gem_name} aprobado para {candidate_id}[/green] (score {score})")

        return result, score, passed

    async def run_gem5(self, search_inputs: dict) -> dict:
        console.print(
            Panel(
                f"[bold cyan]🔍 Ejecutando GEM5 – Radiografía Estratégica[/bold cyan]\nSearch ID: {self.search_id}",
                border_style="cyan",
            )
        )

        async with self._lock:
            completed = "gem5" in self.state["completed_gems"].get("search", [])
            cache = self.state["results_cache"].get("search", {}).get("gem5")

        if completed:
            console.print(
                "[dim]  ⏭️  GEM5 completado previamente. Recuperando de caché...[/dim]"
            )
            return cache

        variables = {
            "search_id": self.search_id,
            **search_inputs,
        }

        with console.status(
            "[cyan]Analizando rol y compañía con IA...[/cyan]", spinner="dots"
        ):
            result = await self._run_gem_with_validation("gem5", variables)

        await self._save_output("gem5", result)
        confidence = (result.get("json") or {}).get("scores", {}).get("confidence")
        console.print(
            f"[bold green]  ✅ GEM5 completado[/bold green] | Confidence: {confidence}"
        )

        return result

    async def run_candidate_pipeline(
        self,
        candidate_id: str,
        candidate_inputs: dict,
        gem5_result: dict,
    ) -> dict:
        # console.print(
        #     Panel(
        #         f"[bold magenta]👤 Procesando Candidato: {candidate_id}[/bold magenta]",
        #         border_style="magenta",
        #     )
        # )

        results: dict[str, Any] = {"candidate_id": candidate_id, "gems": {}}
        gem5_json = gem5_result.get("json", {})
        gem5_content = gem5_json.get("content", {}) if gem5_json else {}

        gem5_summary = (
            json.dumps(gem5_content, ensure_ascii=False)
            if gem5_content
            else gem5_result.get("markdown", "")
        )
        gem5_key_challenge = gem5_content.get(
            "problema_real_del_rol", gem5_result.get("markdown", "No disponible")
        )

        # --- GEM1 ---
        gem1_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "cv_text": candidate_inputs.get("cv_text", "No proporcionado"),
            "interview_notes": candidate_inputs.get(
                "interview_notes", "No proporcionado"
            ),
            "gem5_summary": gem5_summary,
        }
        gem1_result, gem1_score, passed1 = await self._run_generic_gem_step(
            "gem1", candidate_id, gem1_vars, "GEM1 – Trayectoria y Logros"
        )
        results["gems"]["gem1"] = gem1_result
        if not passed1:
            results["decision"] = "DESCARTADO_GEM1"
            return results

        # --- GEM2 ---
        gem2_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "gem1": gem1_result.get("json") or gem1_result.get("raw", ""),
            "tests_text": candidate_inputs.get("tests_text", "No proporcionado"),
            "case_notes": candidate_inputs.get("case_notes", "No proporcionado"),
            "gem5_key_challenge": gem5_key_challenge,
        }
        gem2_result, gem2_score, passed2 = await self._run_generic_gem_step(
            "gem2", candidate_id, gem2_vars, "GEM2 – Assessment a Negocio"
        )
        results["gems"]["gem2"] = gem2_result
        if not passed2:
            results["decision"] = "DESCARTADO_GEM2"
            return results

        # --- GEM3 ---
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
        gem3_result, gem3_score, passed3 = await self._run_generic_gem_step(
            "gem3", candidate_id, gem3_vars, "GEM3 – Veredicto + Referencias 360°"
        )
        results["gems"]["gem3"] = gem3_result
        if not passed3:
            results["decision"] = "DESCARTADO_GEM3"
            return results

        # --- GEM4 ---
        sources = []
        for key in [
            "cv_text",
            "interview_notes",
            "tests_text",
            "case_notes",
            "references_text",
        ]:
            if (
                candidate_inputs.get(key)
                and candidate_inputs[key] != "No proporcionado"
            ):
                sources.append(key)

        gem4_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "gem1": gem1_result.get("json") or gem1_result.get("raw", ""),
            "gem2": gem2_result.get("json") or gem2_result.get("raw", ""),
            "gem3": gem3_result.get("json") or gem3_result.get("raw", ""),
            "sources_index": ", ".join(sources),
        }
        gem4_result, gem4_score, passed4 = await self._run_generic_gem_step(
            "gem4", candidate_id, gem4_vars, "GEM4 – Auditor QA (Gate Final)"
        )
        results["gems"]["gem4"] = gem4_result

        gem4_json = gem4_result.get("json", {})
        decision = (gem4_json or {}).get("decision", "BLOQUEADO")

        if gem4_score is not None and passed4 and decision != "BLOQUEADO":
            decision = "APROBADO"

        results["decision"] = decision
        results["gem4_score"] = gem4_score

        # if decision == "APROBADO":
        #     console.print(
        #         f"\n[bold green]  🎉 REPORTE APROBADO para {candidate_id}[/bold green] (QA score: {gem4_score})"
        #     )
        # else:
        #     console.print(
        #         f"\n[bold red]  🚫 REPORTE BLOQUEADO para {candidate_id}[/bold red] (QA score: {gem4_score})"
        #     )

        return results

    async def run_full_pipeline(
        self, search_inputs: dict, candidates: dict[str, dict]
    ) -> dict:
        timestamp = datetime.now(timezone.utc).isoformat()

        console.rule(
            f"[bold gold1]RAADBot Pipeline Runner v1.5 (Async) – {self.search_id}[/bold gold1]"
        )
        console.print(
            f"[dim]Timestamp: {timestamp} | Candidatos en cola: {len(candidates)}[/dim]\n"
        )

        # 1. GEM5
        gem5_result = await self.run_gem5(search_inputs)

        all_results: dict[str, Any] = {
            "search_id": self.search_id,
            "timestamp": timestamp,
            "gem5": gem5_result,
            "candidates": {},
        }

        # 2. Iterar candidatos en paralelo
        console.print(f"[bold blue]🚀 Procesando {len(candidates)} candidatos en paralelo...[/bold blue]")

        async def process_candidate(cid, cinputs):
            try:
                logger.info(f"👤 Iniciando pipeline para candidato: {cid}")
                return cid, await self.run_candidate_pipeline(cid, cinputs, gem5_result)
            except Exception as e:
                logger.error(f"❌ Error crítico procesando candidato {cid}: {e}", exc_info=True)
                return cid, {
                    "candidate_id": cid,
                    "decision": f"ERROR_EJECUCION: {e}",
                    "gem4_score": None,
                }

        tasks = [process_candidate(cid, cinputs) for cid, cinputs in candidates.items()]
        candidate_results = await asyncio.gather(*tasks)

        for cid, result in candidate_results:
            all_results["candidates"][cid] = result

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
        async with self._lock:
            with open(summary_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)

        # 4. Imprimir Tabla Final Resumen Nivel Psicopata
        self._print_summary(all_results)

        return all_results

    def _print_summary(self, results: dict):
        console.print("\n")

        # Tabla de Candidatos
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

        # Panel de Costos USD
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
