import os
import json
from agent.prompt_builder import load_prompt, clear_prompt_caches
from utils.gem_core import validate_contract

def test_prompt_builder_cache():
    # Write a temporary prompt
    temp_prompt_path = "prompts/temp_test_prompt.md"
    os.makedirs("prompts", exist_ok=True)

    with open(temp_prompt_path, "w", encoding="utf-8") as f:
        f.write("Initial prompt content")

    try:
        # Load initially
        p1 = load_prompt("temp_test_prompt")
        assert p1 == "Initial prompt content"

        # Modify the file, but we keep mtime unchanged (or simulate mtime modification)
        with open(temp_prompt_path, "w", encoding="utf-8") as f:
            f.write("Modified prompt content")

        # Since we modified the file, mtime changes. Let's force-update the modification time
        st = os.stat(temp_prompt_path)
        os.utime(temp_prompt_path, (st.st_atime, st.st_mtime + 5.0))

        p2 = load_prompt("temp_test_prompt")
        assert p2 == "Modified prompt content"

        # Now let's manually clear the caches and check
        clear_prompt_caches()
        p3 = load_prompt("temp_test_prompt")
        assert p3 == "Modified prompt content"

    finally:
        if os.path.exists(temp_prompt_path):
            os.remove(temp_prompt_path)

def test_contract_validation_cache():
    temp_contract_path = "tests/temp_test_contract.json"
    os.makedirs("tests", exist_ok=True)

    contract1 = {"key1": "string"}
    with open(temp_contract_path, "w", encoding="utf-8") as f:
        json.dump(contract1, f)

    try:
        # Validate data
        res1 = validate_contract({"key1": "hello"}, temp_contract_path)
        assert res1 is True

        # Rewrite contract with different schema (requiring 'key2')
        contract2 = {"key2": "number"}
        with open(temp_contract_path, "w", encoding="utf-8") as f:
            json.dump(contract2, f)

        # Update mtime explicitly to ensure the cached loader detects it
        st = os.stat(temp_contract_path)
        os.utime(temp_contract_path, (st.st_atime, st.st_mtime + 5.0))

        # Should now fail since key1 is no longer valid, and key2 is missing
        res2 = validate_contract({"key1": "hello"}, temp_contract_path)
        assert res2 is False

        res3 = validate_contract({"key2": 123}, temp_contract_path)
        assert res3 is True

    finally:
        if os.path.exists(temp_contract_path):
            os.remove(temp_contract_path)
