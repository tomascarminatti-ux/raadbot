from agent.gem6.orchestrator import GEM6Orchestrator
from agent.gemini_client import GeminiClient
from utils.gem_core import GEMClient
import asyncio
import os
import sys
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.getcwd())


async def test_gem6_flow():
    print("🚀 Iniciando Test GEM 6 - Master Orchestrator...")

    # Configuración Mock
    api_key = os.getenv("GEMINI_API_KEY", "dummy_key")
    gemini = GeminiClient(api_key=api_key)
    output_dir = "runs/test_gem6"
    config = {"search_id": "TEST-SEARCH-001"}

    orchestrator = GEM6Orchestrator(gemini, output_dir, config)

    # Inputs Mock
    search_inputs = {"perfil": "CTO para Startup Fintech", "empresa": "RaadAdvisory"}
    candidates = {
        "CAND-001": {
            "candidato_id": "CAND-001",
            "cv_text": "Experiencia liderando equipos de ingeniería...",
            "interview_notes": "Muy técnico, buen fit cultural."
        }
    }

    # Mock behavior of Gemini and GEMClient to avoid network calls during testing
    with patch.object(gemini, 'run_gem') as mock_run_gem, \
         patch.object(GEMClient, 'upsert_entity', return_value=asyncio.Future()) as mock_upsert, \
         patch.object(GEMClient, 'log_execution', return_value=asyncio.Future()) as mock_log:

        mock_run_gem.return_value = {
            "json": {"action": "finalize", "status": "SUCCESS", "thought": "Mocked success"},
            "markdown": "Mocked success",
            "raw": '{"action": "finalize", "status": "SUCCESS"}',
            "usage": {"prompt_tokens": 0, "candidates_tokens": 0, "total_tokens": 0, "finish_reason": "STOP"}
        }

        # Set resolved value for async futures
        mock_upsert.return_value.set_result({"status": "ok"})
        mock_log.return_value.set_result({"status": "ok"})

        # Nota: En un test real sin API Key de verdad, gemini.run_gem fallará o devolverá error.
        # Aquí probamos la estructura de la orquestación con el mock.
        result = await orchestrator.run_pipeline(search_inputs, candidates)

        print("\n✅ Pipeline Ejecutado!")
        print(f"Status: {result['CAND-001']['status']}")

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Aviso: No hay GEMINI_API_KEY. El test ejecutará la lógica pero las llamadas a la API fallarán.")
    asyncio.run(test_gem6_flow())
