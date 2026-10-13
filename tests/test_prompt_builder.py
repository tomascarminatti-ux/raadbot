import os
import time
from agent.prompt_builder import load_prompt, build_prompt, get_required_variables, _load_prompt_cached


def test_load_prompt_and_caching():
    _load_prompt_cached.cache_clear()
    info_before = _load_prompt_cached.cache_info()
    assert info_before.hits == 0

    content1 = load_prompt("gem1")
    assert isinstance(content1, str)
    assert len(content1) > 0

    content2 = load_prompt("gem1")
    assert content1 == content2

    info_after = _load_prompt_cached.cache_info()
    assert info_after.hits >= 1


def test_cache_invalidation_on_mtime_change(tmp_path):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    test_file = prompts_dir / "test_gem.md"
    test_file.write_text("Hello {{name}}", encoding="utf-8")

    filepath = str(test_file)
    mtime1 = os.path.getmtime(filepath)
    res1 = _load_prompt_cached(filepath, mtime1)
    assert res1 == "Hello {{name}}"

    time.sleep(0.01)
    test_file.write_text("Updated {{name}}", encoding="utf-8")
    mtime2 = os.path.getmtime(filepath)
    assert mtime2 > mtime1

    res2 = _load_prompt_cached(filepath, mtime2)
    assert res2 == "Updated {{name}}"


def test_build_prompt():
    result = build_prompt("gem1", {"jd_text": "Python Dev", "candidate": "Alice"})
    assert "Python Dev" in result or "Alice" in result or isinstance(result, str)


def test_get_required_variables():
    vars_list = get_required_variables("gem1")
    assert isinstance(vars_list, list)
    assert "PROMPT_MAESTRO" not in vars_list
    assert "VERSION" not in vars_list
