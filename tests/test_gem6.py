import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.getcwd())

from agent.gemini_client import GeminiClient
from agent.gem6.orchestrator import GEM6Orchestrator

async def test_gem6_flow():
    print("🚀 Iniciando Test GEM 6 - Master Orchestrator...")
    
    # Configuración Mock
    api_key = os.getenv("GEMINI_API_KEY", "dummy_key")
    gemini = GeminiClient(api_key=api_key)

    # Mock run_gem to avoid real API calls in test
    gemini.run_gem = AsyncMock(return_value={
        "json": {"action": "finalize", "status": "SUCCESS", "thought": "Test finished", "final_output": {}},
        "markdown": "Test finished",
        "raw": '{"action": "finalize", "status": "SUCCESS", "thought": "Test finished", "final_output": {}}',
        "usage": {"prompt_tokens": 10, "candidates_tokens": 10, "total_tokens": 20, "finish_reason": "STOP"}
    })

    output_dir = "runs/test_gem6"
    config = {"search_id": "TEST-SEARCH-001"}
    
    orchestrator = GEM6Orchestrator(gemini=gemini, output_dir=output_dir, config=config)
    
    # Inputs Mock
    search_inputs = {"perfil": "CTO para Startup Fintech", "empresa": "RaadAdvisory"}
    candidates = {
        "CAND-001": {
            "cv_text": "Experiencia liderando equipos de ingeniería...",
            "interview_notes": "Muy técnico, buen fit cultural."
        }
    }
    
    try:
        result = await orchestrator.run_pipeline(search_inputs, candidates)
        
        print("\n✅ Pipeline Ejecutado!")
        print(f"Status: {result['CAND-001']['status']}")
        
    except Exception as e:
        print(f"\n❌ Error en el test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gem6_flow())
