import os
import re

import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 1. Pipeline.py Fixes
pipeline_path = "agent/pipeline.py"
with open(pipeline_path, "r") as f:
    pipeline_code = f.read()

# Replace _validate_output to _run_gem_with_validation
new_validation_funcs = """
    def _validate_output(self, json_data: dict, gem_name: str) -> bool:
        if not self.schema or not json_data:
            raise ValueError(f"Output nulo o sin JSON válido en {gem_name}")
        try:
            from jsonschema import validate, ValidationError
            validate(instance=json_data, schema=self.schema)
            return True
        except ValidationError as e:
            raise ValueError(f"Schema fallido en {gem_name}: {e.message}")

    def _get_score(self, json_data: dict) -> int | None:
        if not json_data:
            return None
        scores = json_data.get("scores", {})
        return scores.get("score_dimension")

    def _check_gate(self, gem_name: str, score: int | None) -> bool:
        threshold = THRESHOLDS.get(gem_name)
        if threshold is None:
            return True
        if score is None:
            return False
        return score >= threshold

    def _run_gem_with_validation(self, gem_name: str, prompt_vars: dict) -> dict:
        for attempt in range(MAX_RETRIES_ON_BLOCK + 1):
            prompt = build_prompt(gem_name, prompt_vars)
            result = self.gemini.run_gem(prompt)
            
            try:
                self._validate_output(result.get("json"), gem_name)
                return result
            except ValueError as e:
                import time
                if attempt < MAX_RETRIES_ON_BLOCK:
                    console.print(f"[bold yellow]  ⚠️  Error de validación ({e}). Reintentando {attempt+1}/{MAX_RETRIES_ON_BLOCK}...[/bold yellow]")
                    time.sleep(2)
                else:
                    console.print(f"[bold red]  ❌ Error definitivo de validación en {gem_name}.[/bold red]")
                    return result

    def _run_generic_gem_step(self, gem_name: str, candidate_id: str, prompt_vars: dict, display_name: str) -> tuple[dict, int | None, bool]:
        console.print(f"\\n[bold]📋 {display_name}[/bold]")
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
            console.print(f"[bold red]  ❌ Error parseando score en {gem_name}. Fallo automático.[/bold red]")
            return result, score, False
            
        passed = self._check_gate(gem_name, score)
        if not passed:
            console.print(f"[bold red]  ❌ {gem_name} score ({score}) < {THRESHOLDS.get(gem_name)}. Candidato descartado.[/bold red]")
        else:
            console.print(f"[green]  ✅ {gem_name} aprobado[/green] (score {score})")
            
        return result, score, passed
"""

pipeline_code = re.sub(
    r"    def _validate_output\(self, json_data: dict, gem_name: str\) -> bool:.*?    def run_gem5\(self, search_inputs: dict\) -> dict:",
    new_validation_funcs + "\\n    def run_gem5(self, search_inputs: dict) -> dict:",
    pipeline_code,
    flags=re.DOTALL,
)

new_run_gem5 = """    def run_gem5(self, search_inputs: dict) -> dict:
        console.print(Panel(f"[bold cyan]🔍 Ejecutando GEM5 – Radiografía Estratégica[/bold cyan]\\nSearch ID: {self.search_id}", border_style="cyan"))

        if "gem5" in self.state["completed_gems"].get("search", []):
            console.print("[dim]  ⏭️  GEM5 completado previamente. Recuperando de caché...[/dim]")
            return self.state["results_cache"]["search"]["gem5"]

        variables = {
            "search_id": self.search_id,
            **search_inputs,
        }

        with console.status("[cyan]Analizando rol y compañía con IA...[/cyan]", spinner="dots"):
            result = self._run_gem_with_validation("gem5", variables)

        self._save_output("gem5", result)
        confidence = (result.get("json") or {}).get("scores", {}).get("confidence")
        console.print(f"[bold green]  ✅ GEM5 completado[/bold green] | Confidence: {confidence}")

        return result
"""
pipeline_code = re.sub(
    r"    def run_gem5\(self, search_inputs: dict\) -> dict:.*?    def run_candidate_pipeline\(",
    new_run_gem5 + "\\n    def run_candidate_pipeline(",
    pipeline_code,
    flags=re.DOTALL,
)

new_run_candidate_pipeline = """    def run_candidate_pipeline(
        self,
        candidate_id: str,
        candidate_inputs: dict,
        gem5_result: dict,
    ) -> dict:
        console.print(Panel(f"[bold magenta]👤 Procesando Candidato: {candidate_id}[/bold magenta]", border_style="magenta"))

        results = {"candidate_id": candidate_id, "gems": {}}
        gem5_json = gem5_result.get("json", {})
        gem5_content = gem5_json.get("content", {}) if gem5_json else {}
        import json
        gem5_summary = json.dumps(gem5_content, ensure_ascii=False) if gem5_content else gem5_result.get("markdown", "")
        gem5_key_challenge = gem5_content.get("problema_real_del_rol", gem5_result.get("markdown", "No disponible"))

        # --- GEM1 ---
        gem1_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "cv_text": candidate_inputs.get("cv_text", "No proporcionado"),
            "interview_notes": candidate_inputs.get("interview_notes", "No proporcionado"),
            "gem5_summary": gem5_summary,
        }
        gem1_result, gem1_score, passed1 = self._run_generic_gem_step("gem1", candidate_id, gem1_vars, "GEM1 – Trayectoria y Logros")
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
        gem2_result, gem2_score, passed2 = self._run_generic_gem_step("gem2", candidate_id, gem2_vars, "GEM2 – Assessment a Negocio")
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
            "references_text": candidate_inputs.get("references_text", "No proporcionado"),
            "client_culture": candidate_inputs.get("client_culture", "No proporcionado"),
        }
        gem3_result, gem3_score, passed3 = self._run_generic_gem_step("gem3", candidate_id, gem3_vars, "GEM3 – Veredicto + Referencias 360°")
        results["gems"]["gem3"] = gem3_result
        if not passed3:
            results["decision"] = "DESCARTADO_GEM3"
            return results

        # --- GEM4 ---
        sources = []
        for key in ["cv_text", "interview_notes", "tests_text", "case_notes", "references_text"]:
            if candidate_inputs.get(key) and candidate_inputs[key] != "No proporcionado":
                sources.append(key)
                
        gem4_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "gem1": gem1_result.get("json") or gem1_result.get("raw", ""),
            "gem2": gem2_result.get("json") or gem2_result.get("raw", ""),
            "gem3": gem3_result.get("json") or gem3_result.get("raw", ""),
            "sources_index": ", ".join(sources),
        }
        gem4_result, gem4_score, passed4 = self._run_generic_gem_step("gem4", candidate_id, gem4_vars, "GEM4 – Auditor QA (Gate Final)")
        results["gems"]["gem4"] = gem4_result
        
        gem4_json = gem4_result.get("json", {})
        decision = (gem4_json or {}).get("decision", "BLOQUEADO")
        
        if gem4_score is not None and passed4 and decision != "BLOQUEADO":
            decision = "APROBADO"
            
        results["decision"] = decision
        results["gem4_score"] = gem4_score

        if decision == "APROBADO":
            console.print(f"\\n[bold green]  🎉 REPORTE APROBADO[/bold green] (QA score: {gem4_score})")
        else:
            console.print(f"\\n[bold red]  🚫 REPORTE BLOQUEADO[/bold red] (QA score: {gem4_score}) - Escalando a consultor.")

        return results

    def run_full_pipeline("""
pipeline_code = re.sub(
    r"    def run_candidate_pipeline\([\s\S]*?    def run_full_pipeline\(",
    new_run_candidate_pipeline,
    pipeline_code,
)

with open(pipeline_path, "w") as f:
    f.write(pipeline_code)


# 2. Fix Drive Client
drive_client_path = "agent/drive_client.py"
with open(drive_client_path, "r") as f:
    dc = f.read()

dc = dc.replace(
    """                if mime == "application/pdf" or "wordprocessing" in mime:
                    print(f"  ⚠️  Advertencia: {name} es un archivo binario ({mime}).")
                    print("     El modelo recibirá el texto crudo/binario si no es extraído.")""",
    """                if mime == "application/pdf" or "wordprocessing" in mime:
                    raise ValueError(f"El archivo '{name}' es un binario ({mime}). Por favor súbelo en formato texto (.txt) o como Google Docs exportable. Los PDFs y Word crudos corrompen el output del LLM.")""",
)
with open(drive_client_path, "w") as f:
    f.write(dc)


# 3. Add exact JSON instructions to prompts
for i in range(1, 6):
    prompt_file = f"prompts/gem{i}.md"
    if os.path.exists(prompt_file):
        with open(prompt_file, "a") as f:
            f.write(
                f"""

---
### JSON EXACTO REQUERIDO
DEBES DEVOLVER EXCLUSIVAMENTE UN OBJETO JSON CON LA SIGUIENTE ESTRUCTURA ESTRICTA. No envuelvas las keys en formatos diferentes, no alteres objetos:
```json
{{
  "meta": {{
    "search_id": "{{{{search_id}}}}",
    "candidate_id": "{ "{{candidate_id}}" if i < 5 else "N/A" }",
    "gem": "GEM{i}",
    "timestamp": "ISO 8601",
    "prompt_version": "1.0",
    "sources": ["cv", "interview_notes"]
  }},
  "content": {{ }},
  "scores": {{
    "score_dimension": 8,
    "confidence": "HIGH"
  }},
  "issues_found": []
}}
```
"""
            )

# 4. Requirements fix
reqs = """google-genai==1.2.0
google-api-python-client==2.160.0
google-auth-httplib2==0.2.0
google-auth-oauthlib==1.2.0
jsonschema==4.21.1
python-dotenv==1.0.1
rich==13.7.1
fastapi==0.111.0
uvicorn==0.30.0
httpx==0.27.0
"""
with open("requirements.txt", "w") as f:
    f.write(reqs)
