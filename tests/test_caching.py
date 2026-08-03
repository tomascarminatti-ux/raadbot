import os
import json
from agent.prompt_builder import _load_prompt_cached
from utils.gem_core import _load_contract_cached


def test_prompt_loading_cache_and_invalidation(tmp_path):
    # Setup temporary prompt file in tmp_path
    prompt_file = tmp_path / "test_prompt.md"
    prompt_file.write_text("Hello {{name}}", encoding="utf-8")

    # We need to temporarily point the PROMPTS_DIR or mock the load_prompt behavior,
    # or we can test the internal _load_prompt_cached directly.
    # Let's test _load_prompt_cached directly to prove cache hitting and invalidation.

    filepath = str(prompt_file)
    mtime1 = os.path.getmtime(filepath)

    # 1. Initial Load
    content1 = _load_prompt_cached(filepath, mtime1)
    assert content1 == "Hello {{name}}"

    # Clear the cache info to start clean or check hits
    _load_prompt_cached.cache_clear()

    # Load 1
    _load_prompt_cached(filepath, mtime1)
    # Load 2 (should hit cache)
    _load_prompt_cached(filepath, mtime1)

    hits = _load_prompt_cached.cache_info().hits
    assert hits == 1, f"Expected cache hit, got {hits}"

    # 2. Modify File and Update mtime explicitly using os.utime
    prompt_file.write_text("Hello Updated {{name}}", encoding="utf-8")
    # Advance mtime by 10 seconds to ensure difference
    new_mtime = mtime1 + 10.0
    os.utime(filepath, (new_mtime, new_mtime))

    # Load with new mtime
    content2 = _load_prompt_cached(filepath, new_mtime)
    assert content2 == "Hello Updated {{name}}"

    # This should be a cache miss because mtime changed
    _load_prompt_cached.cache_info()
    # We cleared cache info earlier; let's check overall cache behavior
    # Total calls:
    # 1. Initial Load (after cache_clear): _load_prompt_cached(filepath, mtime1) -> miss
    # 2. Second Load: _load_prompt_cached(filepath, mtime1) -> hit
    # 3. Third Load (new mtime): _load_prompt_cached(filepath, new_mtime) -> miss
    assert _load_prompt_cached.cache_info().hits == 1
    assert _load_prompt_cached.cache_info().misses == 2


def test_contract_loading_cache_and_invalidation(tmp_path):
    contract_file = tmp_path / "test_contract.json"
    schema = {"status": "string"}
    contract_file.write_text(json.dumps(schema), encoding="utf-8")

    filepath = str(contract_file)
    mtime1 = os.path.getmtime(filepath)

    _load_contract_cached.cache_clear()

    # Initial load
    schema1 = _load_contract_cached(filepath, mtime1)
    assert schema1 == schema

    # Second load (hit)
    _load_contract_cached(filepath, mtime1)
    assert _load_contract_cached.cache_info().hits == 1

    # Modify contract and update mtime
    new_schema = {"status": "string", "score": "number"}
    contract_file.write_text(json.dumps(new_schema), encoding="utf-8")
    new_mtime = mtime1 + 10.0
    os.utime(filepath, (new_mtime, new_mtime))

    schema2 = _load_contract_cached(filepath, new_mtime)
    assert schema2 == new_schema
    assert _load_contract_cached.cache_info().misses == 2
