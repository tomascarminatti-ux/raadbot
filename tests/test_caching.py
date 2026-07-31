import os
import json
import time
from utils.gem_core import validate_contract
from agent.prompt_builder import load_prompt, PROMPTS_DIR

def test_contract_cache_and_invalidation():
    # 1. Create a temporary contract
    temp_contract_path = "contracts/test_temp_contract.json"
    os.makedirs("contracts", exist_ok=True)

    # Original schema demands "score" to be a number
    schema_1 = {"score": "number"}
    with open(temp_contract_path, "w") as f:
        json.dump(schema_1, f)

    try:
        # Check validation succeeds for number
        assert validate_contract({"score": 0.85}, temp_contract_path) is True
        # Check validation fails for string
        assert validate_contract({"score": "high"}, temp_contract_path) is False

        # 2. Update contract on disk to demand "score" to be a string
        # Introduce a sleep to guarantee the file's mtime changes (file system mtime resolutions can vary)
        time.sleep(0.01)
        schema_2 = {"score": "string"}
        with open(temp_contract_path, "w") as f:
            json.dump(schema_2, f)

        # Clear Python's file descriptor or cache buffers if any, then validate.
        # Now validation should SUCCEED for string because of automatic cache invalidation
        assert validate_contract({"score": "high"}, temp_contract_path) is True
        # Now validation should FAIL for number because score is expected to be a string
        assert validate_contract({"score": 0.85}, temp_contract_path) is False

    finally:
        if os.path.exists(temp_contract_path):
            os.remove(temp_contract_path)

def test_prompt_cache_and_invalidation():
    # 1. Create a temporary prompt file
    temp_prompt_name = "test_temp_prompt"
    temp_prompt_path = os.path.join(PROMPTS_DIR, f"{temp_prompt_name}.md")

    content_1 = "Original prompt template with {{input}}."
    with open(temp_prompt_path, "w", encoding="utf-8") as f:
        f.write(content_1)

    try:
        # Load prompt and verify content
        assert load_prompt(temp_prompt_name) == content_1

        # 2. Update prompt file on disk
        time.sleep(0.01)
        content_2 = "Updated prompt template with {{input}} and {{extra_var}}."
        with open(temp_prompt_path, "w", encoding="utf-8") as f:
            f.write(content_2)

        # Verify automatic invalidation has loaded the new content
        assert load_prompt(temp_prompt_name) == content_2

    finally:
        if os.path.exists(temp_prompt_path):
            os.remove(temp_prompt_path)
