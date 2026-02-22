import os
import json
import uuid
import asyncio
from typing import Dict, Any, List, Optional
from utils.gem_core import GEMClient, validate_contract, logger
from agent.prompt_builder import build_prompt, build_agent_prompt
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
        
        logger.info(f"Starting AUTONOMOUS orchestration for {entity_id} | Trace: {trace_id}")
        
        working_memory = []
        max_steps = 10
        step = 0
        
        initial_context = {
            "search_inputs": context_data.get("search_inputs", {}),
            "candidate_data": context_data.get("candidate_data", {}),
            "search_id": self.search_id,
            "entity_id": entity_id
        }

        while step < max_steps:
            step += 1
            logger.info(f"Step {step} for {entity_id}")

            # 1. Build GEM 6 prompt with current memory
            prompt = build_prompt("gem6", {
                "search_id": self.search_id,
                "candidate_id": entity_id,
                "context": {
                    **initial_context,
                    "working_memory": working_memory
                }
            })

            # 2. Call GEM 6 for reasoning
            result = self.gemini.run_gem(prompt, gem_name="gem6")
            gem6_decision = result.get("json", {})

            if not gem6_decision:
                logger.error(f"GEM 6 failed to return JSON at step {step}")
                # Log error to DB
                await self.client.log_execution({
                    "entity_id": entity_id,
                    "agent_id": "GEM6",
                    "status": "ERROR",
                    "error": "INVALID_JSON",
                    "trace_id": trace_id
                })
                return {"status": "FAILED", "reason": "GEM6_INVALID_JSON"}

            action = gem6_decision.get("action")
            thought = gem6_decision.get("thought", "No thought provided.")
            logger.info(f"GEM 6 Thought: {thought}")

            if action == "finalize":
                status = gem6_decision.get("status", "SUCCESS")
                final_output = gem6_decision.get("final_output", {})

                # Final State Update
                await self.client.upsert_entity({
                    "entity_id": entity_id,
                    "current_stage": "COMPLETED",
                    "state": status,
                    "agent_responsible": "GEM6",
                    "trace_id": trace_id,
                    "metadata": {"final_thought": thought}
                })

                return {"status": status, "output": final_output, "thought": thought}

            if action == "call_agent":
                agent_id = gem6_decision.get("agent_id")
                payload = gem6_decision.get("payload", {})

                logger.info(f"Executing Agent: {agent_id}")

                # Call specialized agent
                agent_output = await self.call_agent(agent_id, payload)

                # Validation (Contract + Verification)
                contract_path = f"contracts/{agent_id}_output.schema.json"
                is_valid = await self.validate_step(entity_id, agent_id, agent_output, contract_path, trace_id)

                # Update memory
                working_memory.append({
                    "step": step,
                    "agent": agent_id,
                    "thought": thought,
                    "observation": agent_output,
                    "valid_contract": is_valid
                })

                # Log transition to DB
                await self.client.upsert_entity({
                    "entity_id": entity_id,
                    "current_stage": agent_id,
                    "state": "PROCESSING",
                    "agent_responsible": "GEM6",
                    "trace_id": trace_id,
                    "metadata": {"last_thought": thought}
                })
            else:
                logger.warning(f"Unknown action: {action}")
                return {"status": "FAILED", "reason": f"UNKNOWN_ACTION_{action}"}

        return {"status": "FAILED", "reason": "MAX_STEPS_REACHED"}

    async def call_agent(self, agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Calls the agent using GeminiClient or fallback to mock if client missing"""
        logger.info(f"Calling agent {agent_id}")
        
        if self.gemini:
            try:
                # Use prompt_builder for consistent templating
                full_prompt = build_agent_prompt(agent_id, payload)

                result = self.gemini.run_gem(full_prompt, gem_name=agent_id)
                return result.get("json", {}) or {}
            except Exception as e:
                logger.error(f"Error calling Gemini for {agent_id}: {e}")
                return {"error": str(e)}
        
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
        if not os.path.exists(contract_path):
            logger.warning(f"No contract found for {agent_id} at {contract_path}. Skipping strict validation.")
            return True

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
