import asyncio
import os
import sys
from unittest.mock import MagicMock, AsyncMock

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.getcwd())

from agent.gemini_client import GeminiClient  # noqa: E402
from agent.gem6.orchestrator import GEM6Orchestrator  # noqa: E402


async def test_gem6_flow():
    print("🚀 Iniciando Test GEM 6 - Master Orchestrator (MOCKED)...")

    # Mock GeminiClient
    gemini = MagicMock(spec=GeminiClient)
    # Mock GEM 6 decision to finalize immediately
    gemini.run_gem.return_value = {
        "json": {
            "action": "finalize",
            "thought": "Test complete",
            "status": "SUCCESS",
            "final_output": {"score": 10}
        },
        "markdown": "Test complete",
        "raw": "Test complete",
        "usage": {}
    }

    output_dir = "runs/test_gem6"
    config = {"search_id": "TEST-SEARCH-001"}

    orchestrator = GEM6Orchestrator(
        gemini=gemini, output_dir=output_dir, config=config
    )

    # Mock internal client to avoid real HTTP calls
    orchestrator.client = MagicMock()
    orchestrator.client.upsert_entity = AsyncMock()
    orchestrator.client.log_execution = AsyncMock()

    # Inputs Mock
    search_inputs = {
        "perfil": "CTO para Startup Fintech", "empresa": "RaadAdvisory"
    }
    candidates = {
        "CAND-001": {
            "cv_text": "Experiencia liderando equipos de ingeniería...",
            "interview_notes": "Muy técnico, buen fit cultural."
        }
    }

    try:
        # Run the pipeline
        result = await orchestrator.run_pipeline(search_inputs, candidates)

        print("\n✅ Pipeline Ejecutado!")
        print(f"Candidates processed: {list(result.keys())}")
        assert "CAND-001" in result
        assert result["CAND-001"]["status"] == "SUCCESS"

    except Exception as e:
        print(f"\n❌ Error en el test: {e}")
        raise e


if __name__ == "__main__":
    asyncio.run(test_gem6_flow())
