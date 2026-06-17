from agent.gem6.orchestrator import GEM6Orchestrator
from agent.gemini_client import GeminiClient
import asyncio
import os
import sys

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.getcwd())


async def test_gem6_flow():
    print("🚀 Iniciando Test GEM 6 - Master Orchestrator...")

    # Configuración Mock
    api_key = os.getenv("GEMINI_API_KEY", "dummy_key")
    gemini = GeminiClient(api_key=api_key)
    output_dir = "runs/test_gem6"
    config = {"search_id": "TEST-SEARCH-001"}

    from unittest.mock import AsyncMock, MagicMock
    orchestrator = GEM6Orchestrator(gemini, output_dir, config)
    # Mock GEMClient to avoid database calls
    orchestrator.client = MagicMock()
    orchestrator.client.log_execution = AsyncMock(return_value={})
    orchestrator.client.upsert_entity = AsyncMock(return_value={})

    # Mock Gemini run_gem to avoid connection errors
    gemini.run_gem = MagicMock(return_value={
        "json": {"action": "finalize", "status": "SUCCESS", "final_output": {"score": 0.9}},
        "markdown": "Success",
        "raw": '{"action": "finalize", "status": "SUCCESS"}'
    })

    # Inputs Mock
    search_inputs = {"perfil": "CTO para Startup Fintech", "empresa": "RaadAdvisory"}
    candidates = {
        "CAND-001": {
            "cv_text": "Experiencia liderando equipos de ingeniería...",
            "interview_notes": "Muy técnico, buen fit cultural."
        }
    }

    try:
        # Nota: En un test real sin API Key de verdad, gemini.run_gem fallará o devolverá error.
        # Aquí probamos la estructura de la orquestación.
        results = await orchestrator.run_pipeline(search_inputs, candidates)

        print("\n✅ Pipeline Ejecutado!")
        for cid, result in results.items():
            print(f"Candidate: {cid} | Status: {result['status']}")

    except Exception as e:
        print(f"\n❌ Error en el test: {e}")

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Aviso: No hay GEMINI_API_KEY. El test ejecutará la lógica pero las llamadas a la API fallarán.")
    asyncio.run(test_gem6_flow())
