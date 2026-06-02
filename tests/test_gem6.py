import asyncio
import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.getcwd())

from agent.gemini_client import GeminiClient
from agent.gem6.orchestrator import GEM6Orchestrator

@pytest.mark.asyncio
async def test_gem6_parallel_run():
    # Configuración Mock
    gemini = MagicMock(spec=GeminiClient)
    # Mock run_gem to return a finalize decision immediately
    gemini.run_gem.return_value = {
        "json": {
            "thought": "Testing parallel execution",
            "action": "finalize",
            "status": "SUCCESS",
            "final_output": {"score": 0.9}
        }
    }

    output_dir = "runs/test_gem6"
    config = {"search_id": "TEST-SEARCH-001"}
    
    orchestrator = GEM6Orchestrator(gemini, output_dir, config)
    # Mock the DB client to avoid network calls
    orchestrator.client = MagicMock()
    orchestrator.client.upsert_entity = MagicMock(side_effect=lambda x: asyncio.sleep(0))
    orchestrator.client.log_execution = MagicMock(side_effect=lambda x: asyncio.sleep(0))

    # Inputs Mock
    search_inputs = {"perfil": "CTO"}
    # Use dict as expected by run_pipeline
    candidates = {
        "CAND-001": {"cv": "text 1"},
        "CAND-002": {"cv": "text 2"}
    }

    # Run the pipeline
    results = await orchestrator.run_pipeline(search_inputs, candidates)

    # Verify we have results for both candidates
    assert "CAND-001" in results
    assert "CAND-002" in results
    assert results["CAND-001"]["status"] == "SUCCESS"
    assert results["CAND-002"]["status"] == "SUCCESS"
    
    # Verify gemini was called for both (at least once each)
    assert gemini.run_gem.call_count >= 2

if __name__ == "__main__":
    asyncio.run(test_gem6_parallel_run())
