import pytest
import os
import json
from unittest.mock import AsyncMock, MagicMock
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

@pytest.fixture
def mock_gemini():
    client = MagicMock(spec=GeminiClient)
    client.run_gem_async = AsyncMock()
    return client

@pytest.fixture
def temp_output_dir(tmp_path):
    d = tmp_path / "outputs"
    d.mkdir()
    return str(d)

@pytest.mark.asyncio
async def test_pipeline_run_gem5(mock_gemini, temp_output_dir):
    pipeline = Pipeline(mock_gemini, "SEARCH-2026-001", temp_output_dir)

    mock_gemini.run_gem_async.return_value = {
        "json": {
            "meta": {
                "search_id": "SEARCH-2026-001",
                "gem": "GEM_5",
                "prompt_version": "v1.2",
                "timestamp": "2024-01-01T00:00:00Z",
                "sources": ["brief_jd.txt"]
            },
            "scores": {"confidence": 9},
            "blockers": [],
            "content": {"problema_real_del_rol": "Test challenge"}
        },
        "markdown": "# GEM5 Output",
        "usage": {"prompt_tokens": 100, "candidates_tokens": 50}
    }

    search_inputs = {"jd_text": "Need a CEO"}
    result = await pipeline.run_gem5(search_inputs)

    assert result["json"]["scores"]["confidence"] == 9
    assert os.path.exists(os.path.join(temp_output_dir, "gem5.json"))
    assert os.path.exists(os.path.join(temp_output_dir, "pipeline_state.json"))

@pytest.mark.asyncio
async def test_pipeline_full_run_with_descartado(mock_gemini, temp_output_dir):
    pipeline = Pipeline(mock_gemini, "SEARCH-2026-001", temp_output_dir)

    # Mock GEM5
    mock_gemini.run_gem_async.side_effect = [
        # GEM5
        {
            "json": {
                "meta": {"search_id": "SEARCH-2026-001", "gem": "GEM_5", "prompt_version": "v1.2", "timestamp": "2024-01-01T00:00:00Z", "sources": ["s1"]},
                "scores": {"confidence": 8}, "blockers": [], "content": {}
            },
            "usage": {"prompt_tokens": 10, "candidates_tokens": 10}
        },
        # GEM1 for Candidate 1 (fail score)
        {
            "json": {
                "meta": {"search_id": "SEARCH-2026-001", "gem": "GEM_1", "prompt_version": "v1.2", "timestamp": "2024-01-01T00:00:00Z", "sources": ["s1"]},
                "scores": {"score_dimension": 4, "confidence": 8}, "blockers": [], "content": {}
            },
            "usage": {"prompt_tokens": 10, "candidates_tokens": 10}
        }
    ]

    search_inputs = {"jd_text": "jd"}
    candidates = {"CAND-001": {"cv_text": "cv"}}

    results = await pipeline.run_full_pipeline(search_inputs, candidates)

    assert results["candidates"]["CAND-001"]["decision"] == "DESCARTADO_GEM1"
