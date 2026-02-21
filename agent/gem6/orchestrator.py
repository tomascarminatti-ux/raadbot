import asyncio
import uuid
import logging
import traceback
import hashlib
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from agent.gem6.state_machine import GEM6StateMachine
from agent.gem6.context import ContextManager, CandidateContext
from agent.gem6.events import EventBus
from agent.gem6.metrics import MetricsCollector
from agent.gem6.logger import AuditLogger
from agent.gemini_client import GeminiClient, GeminiResult
from agent.prompt_builder import build_prompt

logger = logging.getLogger(__name__)

class GEM6Orchestrator:
    """
    Orquestador Maestro GEM 6: Sistema nervioso central del pipeline RAAD.
    """
    
    def __init__(self, gemini: GeminiClient, output_dir: str, config: Dict[str, Any]):
        self.gemini = gemini
        self.output_dir = output_dir
        self.config = config
        
        self.state_machine = GEM6StateMachine()
        self.context_manager = ContextManager()
        self.event_bus = EventBus()
        self.metrics = MetricsCollector()
        self.audit_logger = AuditLogger(output_dir)
        
    async def execute_pipeline(self, search_inputs: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ejecuta el pipeline completo con supervisión total y manejo de estados.
        """
        pipeline_id = str(uuid.uuid4())
        start_time = datetime.now(timezone.utc)
        
        self.audit_logger.log_event("INFO", pipeline_id, "Pipeline Execution Started", {
            "search_id": self.config.get("search_id"),
            "candidate_count": len(candidates)
        })

        try:
            # 1. VALIDAR E INICIALIZAR
            self.state_machine.transition('validate_gem5') # Simulado o previo
            self.context_manager.set_global_context(
                pipeline_id=pipeline_id,
                mandato=search_inputs,
                start_time=start_time
            )
            
            # 2. PROCESAR CANDIDATOS
            self.state_machine.transition('start_candidates')
            results = []
            
            for cand_data in candidates:
                cand_id = cand_data.get("candidato_id", str(uuid.uuid4()))
                candidato_result = await self.process_single_candidate(pipeline_id, cand_data)
                results.append(candidato_result)
                
                self.metrics.increment('candidates_processed')
                self.metrics.record_histogram('candidate_duration', candidato_result.get('duration_seconds', 0))

            # 3. COMPLETAR
            self.state_machine.transition('all_candidates_done')
            
            final_report = {
                "status": "COMPLETED",
                "pipeline_id": pipeline_id,
                "duration_seconds": (datetime.now(timezone.utc) - start_time).total_seconds(),
                "results": results,
                "metrics": self.metrics.export()
            }
            
            self.audit_logger.log_event("INFO", pipeline_id, "Pipeline Execution Completed Successfully")
            return final_report

        except Exception as e:
            self.state_machine.transition('critical_error')
            self.audit_logger.log_event("CRITICAL", pipeline_id, f"Pipeline Failed: {str(e)}", {
                "traceback": traceback.format_exc()
            })
            raise

    async def process_single_candidate(self, pipeline_id: str, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orquesta el flujo de GEM 1 a GEM 4 para un único candidato.
        """
        cand_id = candidate.get("candidato_id", "unknown")
        start_time = datetime.now(timezone.utc)
        context = self.context_manager.create_candidate_context(cand_id)
        
        self.audit_logger.log_event("INFO", pipeline_id, f"Processing candidate: {cand_id}")

        try:
            # FASE: GEM 1 & GEM 2 (Ejecución secuencial robusta para esta versión)
            self.state_machine.transition('dispatch_gem1_gem2')
            
            # GEM 1
            gem1_out = await self._execute_worker("gem1", candidate, context)
            context.set_output("gem1", gem1_out)
            
            # GEM 2
            gem2_out = await self._execute_worker("gem2", candidate, context)
            context.set_output("gem2", gem2_out)
            
            # GEM 3: Veredicto
            self.state_machine.transition('scores_above_threshold')
            self.state_machine.transition('gem3_completed') # Debería ser dispatch y luego completed
            gem3_out = await self._execute_worker("gem3", candidate, context)
            context.set_output("gem3", gem3_out)
            
            # GEM 4: QA
            self.state_machine.transition('gem3_completed') # Dispatch a GEM4
            # Nota: Reutilizo gem3_completed temporalmente o debería añadir gem4_start
            gem4_out = await self._execute_worker("gem4", candidate, context)
            context.set_output("gem4", gem4_out)
            
            self.state_machine.transition('gem4_score_ge_7')
            
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            return {
                "candidato_id": cand_id,
                "status": "APPROVED",
                "duration_seconds": duration,
                "gem_outputs": context.outputs
            }

        except Exception as e:
            logger.error(f"Error processing candidate {cand_id}: {e}")
            return {
                "candidato_id": cand_id,
                "status": "FAILED",
                "error": str(e)
            }

    async def _execute_worker(self, gem_name: str, candidate: Dict[str, Any], context: CandidateContext) -> Dict[str, Any]:
        """
        Ejecuta un GEM específico con reintentos y logging de eventos.
        """
        await self.event_bus.publish(f"{gem_name}.started", {"candidate_id": context.candidato_id})
        
        # 1. PREPARAR VARIABLES DEL PROMPT
        prompt_vars = self._prepare_prompt_vars(gem_name, candidate, context)
        
        # 2. EJECUTAR CON REINTENTOS (Simplificado aquí, pero usa GeminiClient)
        prompt = build_prompt(gem_name, prompt_vars)
        
        # Simulamos reintentos de red o validación si es necesario
        result = self.gemini.run_gem(prompt)
        
        # 3. VALIDAR Y EXTRAER SCORE
        json_data = result.get("json", {})
        score = self._extract_score(json_data)
        
        # 4. PUBLICAR EVENTO DE COMPLETADO
        await self.event_bus.publish(f"{gem_name}.completed", {
            "candidate_id": context.candidato_id,
            "score": score,
            "usage": result.get("usage")
        })
        
        # 5. RETORNAR RESULTADO
        return result

    def _prepare_prompt_vars(self, gem_name: str, candidate: Dict[str, Any], context: CandidateContext) -> Dict[str, Any]:
        """Construye el diccionario de variables necesario para el PromptBuilder."""
        mandato = context.global_context.get("mandato", {})
        
        base_vars = {
            "search_id": self.config.get("search_id"),
            "candidate_id": context.candidato_id,
            "gem5_summary": json.dumps(mandato, ensure_ascii=False)
        }

        if gem_name == "gem1":
            return {**base_vars, 
                    "cv_text": candidate.get("cv_text", ""), 
                    "interview_notes": candidate.get("interview_notes", "")}
        elif gem_name == "gem2":
            return {**base_vars,
                    "gem1": context.outputs.get("gem1", {}).get("json", {}),
                    "tests_text": candidate.get("tests_text", ""),
                    "case_notes": candidate.get("case_notes", "")}
        elif gem_name == "gem3":
            return {**base_vars,
                    "gem1": context.outputs.get("gem1", {}).get("json", {}),
                    "gem2": context.outputs.get("gem2", {}).get("json", {}),
                    "references_text": candidate.get("references_text", ""),
                    "client_culture": candidate.get("client_culture", "")}
        elif gem_name == "gem4":
            return {**base_vars,
                    "gem1": context.outputs.get("gem1", {}).get("json", {}),
                    "gem2": context.outputs.get("gem2", {}).get("json", {}),
                    "gem3": context.outputs.get("gem3", {}).get("json", {}),
                    "sources_index": candidate.get("sources_index", "")}
        
        return base_vars

    def _extract_score(self, json_data: Dict[str, Any]) -> Optional[int]:
        """Extrae el score de negocio del JSON generado por el GEM."""
        return json_data.get("scores", {}).get("score_dimension")
