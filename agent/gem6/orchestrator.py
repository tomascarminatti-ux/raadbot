import os
import json
import uuid
import asyncio
from typing import Dict, Any, List
from utils.gem_core import GEMClient, validate_contract, logger
import config

class GEM6Orchestrator:
    def __init__(self, *args, **kwargs):
        self.client = GEMClient(os.getenv("DB_API_URL", "http://localhost:8000"))
        self.thresholds = {
            "scoring_cutoff": config.SCORING_CUTOFF,
            "qa_cutoff": config.QA_GATE_CUTOFF
        }
        self.gemini = kwargs.get("gemini") or (args[0] if len(args) > 0 else None)
        self.output_dir = kwargs.get("output_dir") or (args[1] if len(args) > 1 else None)
        self.config = kwargs.get("config") or (args[2] if len(args) > 2 else {})
        self.search_id = kwargs.get("search_id", self.config.get("search_id"))

    async def run_pipeline(self, search_inputs: Dict[str, Any], candidates: Dict[str, Any]):
        """Entry point to process all candidates"""
        results = {}
        for candidate_id, candidate_data in candidates.items():
            context = {
                "search_inputs": search_inputs,
                "candidate_id": candidate_id,
                "candidate_data": candidate_data,
                "entity_id": candidate_id
            }
            results[candidate_id] = await self.process_context(context)
        
        # Save summary
        if self.output_dir:
            os.makedirs(self.output_dir, exist_ok=True)
            summary_path = os.path.join(self.output_dir, "pipeline_summary.json")
            summary = {
                "search_id": self.search_id,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "candidates": results
            }
            with open(summary_path, "w") as f:
                json.dump(summary, f, indent=2)
        
        return results

    async def process_context(self, context_data: Dict[str, Any]):
        trace_id = str(uuid.uuid4())
        entity_id = context_data.get("entity_id", "unknown")
        
        logger.info(f"Starting orchestration for {entity_id} | Trace: {trace_id}")
        
        # 1. GEM1: Discovery
        gem1_output = await self.call_agent("gem1", context_data)
        if not await self.validate_step(entity_id, "GEM1", gem1_output, "contracts/gem1_output.schema.json", trace_id):
            return {"status": "FAILED", "reason": "GEM1_CONTRACT_VIOLATION"}

        # 2. GEM2: Scoring
        gem2_output = await self.call_agent("gem2", gem1_output)
        score = gem2_output.get("score", 0)
        
        if score < self.thresholds["scoring_cutoff"]:
            await self.client.discard_entity({
                "entity_id": entity_id,
                "stage_at_discard": "GEM2",
                "reason": f"Low score: {score}",
                "score_at_discard": float(score),
                "agent_responsible": "GEM2",
                "trace_id": trace_id
            })
            return {"status": "DISCARDED", "reason": "LOW_SCORE", "score": score}

        # 3. GEM3: Decision
        gem3_output = await self.call_agent("gem3", gem2_output)
        if not await self.validate_step(entity_id, "GEM3", gem3_output, "contracts/gem3_output.schema.json", trace_id):
            return {"status": "FAILED", "reason": "GEM3_CONTRACT_VIOLATION"}

        # 4. GEM4: QA Gate
        gem4_output = await self.call_agent("gem4", gem3_output)
        qa_score = gem4_output.get("qa_score", 0)
        
        if qa_score < self.thresholds["qa_cutoff"]:
            await self.client.upsert_entity({
                "entity_id": entity_id,
                "current_stage": "GEM4",
                "state": "REVIEW_REQUIRED",
                "human_required": True,
                "agent_responsible": "GEM4",
                "trace_id": trace_id,
                "last_score": float(qa_score)
            })
            return {"status": "HUMAN_REVIEW", "reason": f"Low QA score: {qa_score}", "qa_score": qa_score}

        # Final Success
        await self.client.upsert_entity({
            "entity_id": entity_id,
            "current_stage": "COMPLETED",
            "state": "SUCCESS",
            "agent_responsible": "GEM6",
            "trace_id": trace_id,
            "last_score": float(qa_score)
        })
        return {"status": "SUCCESS", "qa_score": qa_score}

    async def call_agent(self, agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Calls the agent using GeminiClient or fallback to mock if client missing"""
        logger.info(f"Calling agent {agent_id}")
        
        if self.gemini:
            # Real LLM call
            # In a real system, we'd load a specific prompt for the agent
            prompt_file = f"prompts/{agent_id}.md"
            system_prompt = ""
            if os.path.exists(prompt_file):
                with open(prompt_file, "r") as f:
                    system_prompt = f.read()
            
            full_prompt = f"{system_prompt}\n\nINPUT DATA:\n{json.dumps(payload)}\n\nRespond strictly in JSON."
            
            try:
                # Assuming GeminiClient.run_gem returns a dict with 'data'
                result = self.gemini.run_gem(full_prompt, gem_name=agent_id)
                return result.get("data", {})
            except Exception as e:
                logger.error(f"Error calling Gemini for {agent_id}: {e}")
                return {}
        
        # Fallback to mock for local testing/demo if no Gemini client
        await asyncio.sleep(0.1)
        if agent_id == "gem1":
            return {"discovery_dataset": ["item1"], "confidence_score": 0.9, "execution_metadata": {}}
        if agent_id == "gem2":
            return {"score": 0.85}
        if agent_id == "gem3":
            return {"decision": "ACCEPT", "decision_confidence": 0.95, "reasoning_summary": "Meets all criteria"}
        if agent_id == "gem4":
            return {"qa_score": 0.98, "issues": [], "human_required": False}
        return {}

    async def validate_step(self, entity_id, agent_id, output, contract_path, trace_id):
        is_ok = validate_contract(output, contract_path)
        await self.client.log_execution({
            "entity_id": entity_id,
            "agent_id": agent_id,
            "input_ok": True,
            "output_ok": is_ok,
            "time_ms": 100,
            "status": "OK" if is_ok else "CONTRACT_ERROR",
            "trace_id": trace_id
        })
        return is_ok

if __name__ == "__main__":
    import time
    orch = GEM6Orchestrator()
    # Mock trigger
    asyncio.run(orch.process_context({"entity_id": "TEST-001", "context": "Discovery request"}))
