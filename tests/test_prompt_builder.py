import os
import time
import pytest
from unittest.mock import patch
from agent.prompt_builder import (
    load_prompt,
    load_maestro,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_and_caching(tmp_path):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    prompt_file = prompts_dir / "gem_test.md"
    prompt_file.write_text("Hello {{name}}!", encoding="utf-8")

    with patch("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir)):
        _load_prompt_cached.cache_clear()

        content1 = load_prompt("gem_test")
        assert content1 == "Hello {{name}}!"

        info1 = _load_prompt_cached.cache_info()
        assert info1.hits == 0

        content2 = load_prompt("gem_test")
        assert content2 == "Hello {{name}}!"

        info2 = _load_prompt_cached.cache_info()
        assert info2.hits == 1

        # Modify file and update mtime to test cache invalidation
        time.sleep(0.01)
        prompt_file.write_text("Updated {{name}}!", encoding="utf-8")
        new_mtime = time.time() + 10
        os.utime(str(prompt_file), (new_mtime, new_mtime))

        content3 = load_prompt("gem_test")
        assert content3 == "Updated {{name}}!"


def test_load_prompt_not_found():
    with pytest.raises(FileNotFoundError):
        load_prompt("non_existent_gem_xyz")


def test_build_prompt_integration():
    vars_gem1 = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced Dev",
        "interview_notes": "Great fit",
        "gem5_summary": "Role summary",
    }
    result = build_prompt("gem1", vars_gem1)
    assert "SEARCH-001" in result
    assert "CAND-001" in result
    assert "Experienced Dev" in result


def test_get_required_variables():
    required = get_required_variables("gem1")
    assert "search_id" in required
    assert "candidate_id" in required
    assert "PROMPT_MAESTRO" not in required
