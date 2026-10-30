import asyncio
import os
import sys
from datetime import datetime, timezone

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.getcwd())

from agent.gemini_client import GeminiClient
from agent.gem6.orchestrator import GEM6Orchestrator

class MockGeminiClient:
    def run_gem(self, prompt, gem_name=None):
        return {
            "json": {
                "action": "finalize",
                "status": "SUCCESS",
                "thought": "Candidato evaluado con éxito en orquestación paralela.",
                "final_output": {"score": 0.95}
            },
            "markdown": "Orquestación finalizada.",
            "raw": ""
        }

async def test_gem6_flow():
    print("🚀 Iniciando Test GEM 6 - Master Orchestrator...")
    
    # Configuración Mock
    gemini = MockGeminiClient()
    output_dir = "runs/test_gem6"
    config = {"search_id": "TEST-SEARCH-001"}
    
    orchestrator = GEM6Orchestrator(gemini, output_dir, config)
    
    # Inputs Mock con múltiples candidatos
    search_inputs = {"perfil": "CTO para Startup Fintech", "empresa": "RaadAdvisory"}
    candidates = [
        {
            "candidato_id": "CAND-001",
            "cv_text": "Experiencia liderando equipos de ingeniería...",
            "interview_notes": "Muy técnico, buen fit cultural."
        },
        {
            "candidato_id": "CAND-002",
            "cv_text": "Experiencia en arquitectura distribuida...",
            "interview_notes": "Gran experiencia en escalabilidad."
        }
    ]
    
    result = await orchestrator.execute_pipeline(search_inputs, candidates)
    assert result["status"] == "success"
    assert result["search_id"] == "TEST-SEARCH-001"
    assert result["metrics"]["counters"]["candidates_processed"] == 2

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Aviso: No hay GEMINI_API_KEY. El test ejecutará la lógica pero las llamadas a la API fallarán.")
    asyncio.run(test_gem6_flow())
