import json
import os
import time
import pytest
from utils.gem_core import validate_contract, _load_contract_cached
from agent.prompt_builder import load_prompt, build_prompt, _read_prompt_file, PROMPTS_DIR


def test_contract_validation_cache(tmp_path):
    contract_file = tmp_path / "test_contract.json"
    schema = {"name": "string", "score": "number"}
    contract_file.write_text(json.dumps(schema), encoding="utf-8")

    data = {"name": "Test User", "score": 95}
    assert validate_contract(data, str(contract_file)) is True

    # Check cache info
    cache_info_before = _load_contract_cached.cache_info()
    assert cache_info_before.currsize > 0

    # Second call should hit the cache
    assert validate_contract(data, str(contract_file)) is True
    cache_info_after = _load_contract_cached.cache_info()
    assert cache_info_after.hits > cache_info_before.hits

    # Update contract on disk and explicitly update mtime
    new_schema = {"name": "string", "score": "number", "role": "string"}
    contract_file.write_text(json.dumps(new_schema), encoding="utf-8")
    future_time = time.time() + 5
    os.utime(str(contract_file), (future_time, future_time))

    # Without 'role', validation should now fail
    assert validate_contract(data, str(contract_file)) is False

    # With 'role', validation passes
    data_with_role = {"name": "Test User", "score": 95, "role": "Admin"}
    assert validate_contract(data_with_role, str(contract_file)) is True


def test_prompt_builder_cache(tmp_path, monkeypatch):
    test_prompts_dir = tmp_path / "prompts"
    test_prompts_dir.mkdir()

    maestro_file = test_prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("Maestro Context", encoding="utf-8")

    prompt_file = test_prompts_dir / "gem_test.md"
    prompt_file.write_text("Hello {{PROMPT_MAESTRO}} - {{name}}!", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(test_prompts_dir))

    # Initial load and prompt build
    prompt_text = load_prompt("gem_test")
    assert prompt_text == "Hello {{PROMPT_MAESTRO}} - {{name}}!"

    built = build_prompt("gem_test", {"name": "Alice"})
    assert built == "Hello Maestro Context - Alice!"

    cache_info_before = _read_prompt_file.cache_info()

    # Second load hits cache
    load_prompt("gem_test")
    cache_info_after = _read_prompt_file.cache_info()
    assert cache_info_after.hits > cache_info_before.hits

    # Update prompt file on disk with updated mtime
    prompt_file.write_text("Updated {{PROMPT_MAESTRO}} for {{name}}!", encoding="utf-8")
    future_time = time.time() + 5
    os.utime(str(prompt_file), (future_time, future_time))

    built_updated = build_prompt("gem_test", {"name": "Bob"})
    assert built_updated == "Updated Maestro Context for Bob!"
