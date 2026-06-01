import asyncio
import os
import sys
import time
from unittest.mock import MagicMock, patch

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.getcwd())

from agent.gemini_client import GeminiClient
from agent.gem6.orchestrator import GEM6Orchestrator

async def test_gem6_flow():
    print("🚀 Iniciando Test GEM 6 - Master Orchestrator...")
    
    # Configuración Mock
    api_key = "dummy_key"
    gemini = GeminiClient(api_key=api_key)
    output_dir = "runs/test_gem6"
    config = {"search_id": "TEST-SEARCH-001"}
    
    # Mocking run_gem to simulate LLM responses and delay
    async def mocked_run_gem(prompt, gem_name=None):
        # Simulate LLM processing time
        await asyncio.sleep(0.5)
        if gem_name == "gem6":
            return {"json": {"action": "finalize", "status": "SUCCESS", "thought": "Test complete"}}
        return {"json": {"status": "OK"}}

    # Use patch to mock asyncio.to_thread which calls gemini.run_gem
    # In orchestrator.py it is called as: await asyncio.to_thread(self.gemini.run_gem, prompt, gem_name="gem6")

    orchestrator = GEM6Orchestrator(gemini, output_dir, config)
    
    # Mock the gemini.run_gem itself
    gemini.run_gem = MagicMock(side_effect=lambda *args, **kwargs: {
        "json": {"action": "finalize", "status": "SUCCESS", "thought": "Test complete"}
    })

    # We want to measure if parallelization works.
    # If we have 3 candidates and each takes 0.5s, sequential would be 1.5s, parallel ~0.5s.

    # Update mock to include sleep
    def sync_mocked_run_gem(*args, **kwargs):
        time.sleep(0.5)
        return {"json": {"action": "finalize", "status": "SUCCESS", "thought": "Test complete"}}

    gemini.run_gem = MagicMock(side_effect=sync_mocked_run_gem)

    # Inputs Mock
    search_inputs = {"perfil": "CTO for Startup", "empresa": "RaadAdvisory"}
    candidates = {
        "CAND-001": {"cv_text": "Experienced dev..."},
        "CAND-002": {"cv_text": "Tech lead..."},
        "CAND-003": {"cv_text": "CTO..."},
    }
    
    start_time = time.time()
    try:
        print(f"Processing {len(candidates)} candidates...")
        results = await orchestrator.run_pipeline(search_inputs, candidates)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"\n✅ Pipeline Ejecutado en {duration:.2f} segundos!")
        
        # If parallel, duration should be significantly less than 1.5s (3 * 0.5s)
        if duration < 1.0:
            print("⚡ Optimization Verified: Candidates processed in parallel!")
        else:
            print("🐢 Optimization Failed: Processing seems sequential.")

        for cid, res in results.items():
            print(f"Candidate {cid}: {res['status']}")

    except Exception as e:
        print(f"\n❌ Error en el test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gem6_flow())
