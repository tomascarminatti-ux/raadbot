import asyncio
import os
import sys
from unittest.mock import AsyncMock

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.getcwd())

from agent.gem6.orchestrator import GEM6Orchestrator  # noqa: E402


async def test_gem6_flow():
    print("🚀 Iniciando Test GEM 6 - Master Orchestrator...")

    # Configuración Mock
    mock_gemini = AsyncMock()
    # Mocking GEM6 reasoning response
    mock_gemini.run_gem.return_value = {
        "json": {
            "thought": "All done",
            "action": "finalize",
            "status": "SUCCESS",
            "final_output": {"result": "ok"}
        }
    }

    output_dir = "runs/test_gem6"
    config = {"search_id": "TEST-SEARCH-001"}

    orchestrator = GEM6Orchestrator(mock_gemini, output_dir, config)

    # Mock database client to avoid real network calls
    orchestrator.client = AsyncMock()
    orchestrator.client.upsert_entity.return_value = {"status": "success"}
    orchestrator.client.log_execution.return_value = {"status": "logged"}
    orchestrator.client.close.return_value = None

    # Inputs Mock
    search_inputs = {"perfil": "CTO para Startup Fintech", "empresa": "RaadAdvisory"}
    candidates = {
        "CAND-001": {
            "cv_text": "Experiencia liderando equipos de ingeniería...",
            "interview_notes": "Muy técnico, buen fit cultural."
        }
    }

    try:
        # Aquí probamos la estructura de la orquestación con mocks.
        result = await orchestrator.run_pipeline(search_inputs, candidates)

        print("\n✅ Pipeline Ejecutado!")
        assert "CAND-001" in result
        assert result["CAND-001"]["status"] == "SUCCESS"

    except Exception as e:
        print(f"\n❌ Error en el test: {e}")
        raise e


if __name__ == "__main__":
    asyncio.run(test_gem6_flow())
