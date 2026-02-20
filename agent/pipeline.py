"""
pipeline.py – Orquestador del pipeline GEM de RAAD.

Ejecuta secuencialmente: GEM5 → GEM1 → GEM2 → GEM3 → GEM4
con gating por score y flujo post-bloqueo.
"""

import json
import os
from datetime import datetime, timezone

from jsonschema import validate, ValidationError

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


class Pipeline:
    """Orquestador del pipeline GEM."""

    def __init__(self, gemini: GeminiClient, search_id: str, output_dir: str):
        self.gemini = gemini
        self.search_id = search_id
        self.output_dir = output_dir
        self.schema = self._load_schema()

        os.makedirs(output_dir, exist_ok=True)

    def _load_schema(self) -> dict | None:
        schema_path = os.path.join(
            os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
        )
        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def _save_output(self, gem_name: str, result: dict, candidate_id: str = None):
        """Guarda output JSON y Markdown."""
        prefix = gem_name
        if candidate_id:
            candidate_dir = os.path.join(self.output_dir, candidate_id)
            os.makedirs(candidate_dir, exist_ok=True)
            base = candidate_dir
        else:
            base = self.output_dir

        # JSON
        json_path = os.path.join(base, f"{prefix}.json")
        if result.get("json"):
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result["json"], f, ensure_ascii=False, indent=2)

        # Markdown
        md_path = os.path.join(base, f"{prefix}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(result.get("markdown", result.get("raw", "")))

        # Raw (backup)
        raw_path = os.path.join(base, f"{prefix}.raw.txt")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(result.get("raw", ""))

        return json_path, md_path

    def _validate_output(self, json_data: dict, gem_name: str) -> bool:
        """Valida output contra JSON Schema."""
        if not self.schema or not json_data:
            return True

        try:
            validate(instance=json_data, schema=self.schema)
            return True
        except ValidationError as e:
            print(f"  ⚠️  Schema validation warning ({gem_name}): {e.message}")
            return False

    def _get_score(self, json_data: dict) -> int | None:
        """Extrae score_dimension del output JSON."""
        if not json_data:
            return None
        scores = json_data.get("scores", {})
        return scores.get("score_dimension")

    def _check_gate(self, gem_name: str, score: int | None) -> bool:
        """Verifica si el score pasa el threshold."""
        threshold = THRESHOLDS.get(gem_name)
        if threshold is None or score is None:
            return True
        return score >= threshold

    def run_gem5(self, search_inputs: dict) -> dict:
        """Ejecuta GEM5 – Radiografía Estratégica."""
        print("\n" + "=" * 60)
        print("🔍 GEM5 – Radiografía Estratégica")
        print("=" * 60)

        variables = {
            "search_id": self.search_id,
            **search_inputs,
        }

        prompt = build_prompt("gem5", variables)
        result = self.gemini.run_gem(prompt)

        self._save_output("gem5", result)
        self._validate_output(result.get("json"), "gem5")

        confidence = (result.get("json") or {}).get("scores", {}).get("confidence")
        print(f"  ✅ GEM5 completado | Confidence: {confidence}")

        return result

    def run_candidate_pipeline(
        self,
        candidate_id: str,
        candidate_inputs: dict,
        gem5_result: dict,
    ) -> dict:
        """
        Ejecuta el pipeline completo para un candidato:
        GEM1 → GEM2 → GEM3 → GEM4

        Returns:
            dict con resultados de cada GEM y decisión final
        """
        print(f"\n{'=' * 60}")
        print(f"👤 Candidato: {candidate_id}")
        print(f"{'=' * 60}")

        results = {"candidate_id": candidate_id, "gems": {}}
        gem5_json = gem5_result.get("json", {})
        gem5_content = gem5_json.get("content", {}) if gem5_json else {}

        # --- GEM1: Trayectoria y Logros ---
        print("\n📋 GEM1 – Trayectoria y Logros")
        gem1_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "cv_text": candidate_inputs.get("cv_text", "No proporcionado"),
            "interview_notes": candidate_inputs.get(
                "interview_notes", "No proporcionado"
            ),
            "gem5_summary": json.dumps(gem5_content, ensure_ascii=False)
            if gem5_content
            else gem5_result.get("markdown", ""),
        }

        gem1_prompt = build_prompt("gem1", gem1_vars)
        gem1_result = self.gemini.run_gem(gem1_prompt)
        self._save_output("gem1", gem1_result, candidate_id)
        results["gems"]["gem1"] = gem1_result

        gem1_score = self._get_score(gem1_result.get("json"))
        print(f"  Score: {gem1_score}")

        if not self._check_gate("gem1", gem1_score):
            print(f"  ❌ GEM1 score ({gem1_score}) < 6. Candidato descartado.")
            results["decision"] = "DESCARTADO_GEM1"
            return results

        print(f"  ✅ GEM1 aprobado (score {gem1_score} ≥ 6)")

        # --- GEM2: Assessment a Negocio ---
        print("\n🧠 GEM2 – Assessment a Negocio")
        gem2_vars = {
            "search_id": self.search_id,
            "candidate_id": candidate_id,
            "gem1": gem1_result.get("json") or gem1_result.get("raw", ""),
            "tests_text": candidate_inputs.get("tests_text", "No proporcionado"),
            "case_notes": candidate_inputs.get("case_notes", "No proporcionado"),
            "gem5_key_challenge": gem5_content.get(
                "problema_real_del_rol",
                gem5_result.get("markdown", "No disponible"),
            ),
        }

        gem2_prompt = build_prompt("gem2", gem2_vars)
        gem2_result = self.gemini.run_gem(gem2_prompt)
        self._save_output("gem2", gem2_result, candidate_id)
        results["gems"]["gem2"] = gem2_result

        gem2_score = self._get_score(gem2_result.get("json"))
        print(f"  Score: {gem2_score}")

        if not self._check_gate("gem2", gem2_score):
            print(f"  ❌ GEM2 score ({gem2_score}) < 6. Candidato descartado.")
            results["decision"] = "DESCARTADO_GEM2"
            return results

        print(f"  ✅ GEM2 aprobado (score {gem2_score} ≥ 6)")

        # --- GEM3: Veredicto + Referencias 360° ---
        print("\n🔎 GEM3 – Veredicto + Referencias 360°")
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

        gem3_prompt = build_prompt("gem3", gem3_vars)
        gem3_result = self.gemini.run_gem(gem3_prompt)
        self._save_output("gem3", gem3_result, candidate_id)
        results["gems"]["gem3"] = gem3_result

        gem3_score = self._get_score(gem3_result.get("json"))
        print(f"  Score: {gem3_score}")

        if not self._check_gate("gem3", gem3_score):
            print(f"  ❌ GEM3 score ({gem3_score}) < 6. Candidato descartado.")
            results["decision"] = "DESCARTADO_GEM3"
            return results

        print(f"  ✅ GEM3 aprobado (score {gem3_score} ≥ 6)")

        # --- GEM4: Auditor QA ---
        print("\n🛡️  GEM4 – Auditor QA (Gate Final)")

        # Construir índice de fuentes
        sources = []
        for key in ["cv_text", "interview_notes", "tests_text", "case_notes", "references_text"]:
            if candidate_inputs.get(key) and candidate_inputs[key] != "No proporcionado":
                sources.append(key)

        gem4_result = self._run_gem4_with_retries(
            candidate_id, gem1_result, gem2_result, gem3_result, sources
        )
        results["gems"]["gem4"] = gem4_result

        gem4_json = gem4_result.get("json", {})
        decision = (gem4_json or {}).get("decision", "DESCONOCIDO")
        gem4_score = self._get_score(gem4_json)

        results["decision"] = decision
        results["gem4_score"] = gem4_score

        if decision == "APROBADO":
            print(f"\n  🎉 REPORTE APROBADO (QA score: {gem4_score})")
        else:
            print(f"\n  🚫 REPORTE BLOQUEADO (QA score: {gem4_score})")

        return results

    def _run_gem4_with_retries(
        self,
        candidate_id: str,
        gem1_result: dict,
        gem2_result: dict,
        gem3_result: dict,
        sources: list,
        attempt: int = 0,
    ) -> dict:
        """Ejecuta GEM4 con reintentos post-bloqueo."""
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
        self._save_output("gem4", gem4_result, candidate_id)

        gem4_json = gem4_result.get("json", {})
        gem4_score = self._get_score(gem4_json)
        decision = (gem4_json or {}).get("decision", "BLOQUEADO")

        print(f"  Score QA: {gem4_score} | Decisión: {decision}")

        if decision != "BLOQUEADO" and self._check_gate("gem4", gem4_score):
            return gem4_result

        if attempt < MAX_RETRIES_ON_BLOCK:
            print(
                f"  🔄 Intento {attempt + 1}/{MAX_RETRIES_ON_BLOCK} de corrección..."
            )
            # En un sistema más avanzado, aquí se re-ejecutarían los GEMs afectados
            # Por ahora, re-ejecutamos GEM4 esperando un resultado diferente
            return self._run_gem4_with_retries(
                candidate_id,
                gem1_result,
                gem2_result,
                gem3_result,
                sources,
                attempt + 1,
            )

        print("  ⛔ Máximo de reintentos alcanzado. Escalando a consultor senior.")
        return gem4_result

    def run_full_pipeline(
        self,
        search_inputs: dict,
        candidates: dict[str, dict],
    ) -> dict:
        """
        Ejecuta el pipeline completo: GEM5 + todos los candidatos.

        Args:
            search_inputs: dict con jd_text, kickoff_notes, company_context
            candidates: dict de candidate_id → dict con inputs del candidato

        Returns:
            dict con resultados de la búsqueda completa
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        print(f"\n{'#' * 60}")
        print(f"# RAAD Pipeline – {self.search_id}")
        print(f"# {timestamp}")
        print(f"# Candidatos: {len(candidates)}")
        print(f"{'#' * 60}")

        # 1. GEM5
        gem5_result = self.run_gem5(search_inputs)

        # 2. Pipeline por candidato
        all_results = {
            "search_id": self.search_id,
            "timestamp": timestamp,
            "gem5": gem5_result,
            "candidates": {},
        }

        for candidate_id, candidate_inputs in candidates.items():
            result = self.run_candidate_pipeline(
                candidate_id, candidate_inputs, gem5_result
            )
            all_results["candidates"][candidate_id] = result

        # 3. Resumen final
        self._print_summary(all_results)

        # 4. Guardar resumen
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

        return all_results

    def _print_summary(self, results: dict):
        """Imprime resumen final del pipeline."""
        print(f"\n{'=' * 60}")
        print("📊 RESUMEN FINAL")
        print(f"{'=' * 60}")

        for cid, cresult in results["candidates"].items():
            decision = cresult.get("decision", "?")
            score = cresult.get("gem4_score", "?")
            icon = "✅" if decision == "APROBADO" else "❌" if "DESCARTADO" in str(decision) else "🚫"
            print(f"  {icon} {cid}: {decision} (QA: {score})")

        print(f"{'=' * 60}")
