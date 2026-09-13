import pytest
from unittest.mock import MagicMock
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

def test_pipeline_compiled_validator(tmp_path):
    mock_gemini = MagicMock(spec=GeminiClient)
    pipeline = Pipeline(mock_gemini, "SEARCH-2026-001", str(tmp_path))

    assert pipeline.validator is not None

    valid_json = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "gem": "GEM_1",
            "prompt_version": "v1.2",
            "timestamp": "2026-01-01T00:00:00Z",
            "sources": ["cv.txt"]
        },
        "scores": {"confidence": 9},
        "blockers": [],
        "content": {}
    }

    assert pipeline._validate_output(valid_json, "gem1") is True

    invalid_json = {"invalid": "data"}
    with pytest.raises(ValueError, match="Schema fallido en gem1"):
        pipeline._validate_output(invalid_json, "gem1")
