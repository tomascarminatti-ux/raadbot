import pytest
import os
from unittest.mock import MagicMock
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

def test_get_cached_validator(tmp_path):
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()

    mock_gemini = MagicMock(spec=GeminiClient)
    pipeline = Pipeline(mock_gemini, "SEARCH-2026-001", str(output_dir))

    # Assert that the validator was indeed compiled and is not None
    assert pipeline.validator is not None

    # Assert validation is successful for correct data
    valid_data = {
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
    }

    assert pipeline._validate_output(valid_data, "gem5") is True
