import pytest
from unittest.mock import MagicMock
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

@pytest.fixture
def mock_gemini():
    client = MagicMock(spec=GeminiClient)
    return client

def test_pipeline_compiled_validator_initialization(mock_gemini, tmp_path):
    pipeline = Pipeline(mock_gemini, "SEARCH-2026-001", str(tmp_path))
    assert pipeline.validator is not None

def test_pipeline_compiled_validator_validation(mock_gemini, tmp_path):
    pipeline = Pipeline(mock_gemini, "SEARCH-2026-001", str(tmp_path))

    valid_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2026-01-01T00:00:00Z",
            "sources": ["cv_text"]
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9
        },
        "blockers": [],
        "content": {"summary": "Valid content"}
    }

    # Validation should return True for valid payload
    assert pipeline._validate_output(valid_data, "gem1") is True

    invalid_data = {
        "meta": {
            "search_id": "invalid_search_format"
        }
    }

    # Validation should raise ValueError for invalid payload
    with pytest.raises(ValueError, match="Schema fallido en gem1"):
        pipeline._validate_output(invalid_data, "gem1")
