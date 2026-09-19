import pytest
import json
import os
import time
import httpx
from utils.gem_core import validate_contract, GEMClient, _load_contract_cached

def test_validate_contract_types():
    # Create temp contract
    contract = {
        "name": "string",
        "score": "number",
        "is_active": "boolean",
        "tags": "array",
        "metadata": "object"
    }
    contract_path = "tests/temp_contract.json"
    os.makedirs("tests", exist_ok=True)
    with open(contract_path, "w") as f:
        json.dump(contract, f)
    
    # Valid data
    valid_data = {
        "name": "Test",
        "score": 0.9,
        "is_active": True,
        "tags": ["a", "b"],
        "metadata": {"key": "value"}
    }
    assert validate_contract(valid_data, contract_path) is True
    
    # Invalid type
    invalid_data = valid_data.copy()
    invalid_data["score"] = "high"
    assert validate_contract(invalid_data, contract_path) is False
    
    # Missing key
    missing_data = valid_data.copy()
    missing_data.pop("name", None)
    assert validate_contract(missing_data, contract_path) is False

    # Cleanup
    if os.path.exists(contract_path):
        os.remove(contract_path)

def test_validate_contract_cache_and_invalidation():
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)

    initial_contract = {"field_a": "string"}
    with open(contract_path, "w") as f:
        json.dump(initial_contract, f)

    _load_contract_cached.cache_clear()

    # First validation
    assert validate_contract({"field_a": "hello"}, contract_path) is True
    assert validate_contract({"field_b": "hello"}, contract_path) is False

    # Modify file and update mtime
    updated_contract = {"field_b": "string"}
    with open(contract_path, "w") as f:
        json.dump(updated_contract, f)

    # Explicitly change mtime to trigger cache invalidation
    new_mtime = time.time() + 10.0
    os.utime(contract_path, (new_mtime, new_mtime))

    # Should pick up updated schema after mtime change
    assert validate_contract({"field_b": "hello"}, contract_path) is True
    assert validate_contract({"field_a": "hello"}, contract_path) is False

    if os.path.exists(contract_path):
        os.remove(contract_path)

@pytest.mark.asyncio
async def test_gem_client_connection_reuse():
    mock_client = httpx.AsyncClient()
    gem_client = GEMClient(db_url="http://localhost:9999", client=mock_client)

    assert gem_client._get_client() is mock_client

    await gem_client.close()
    assert mock_client.is_closed is True

def test_real_contracts():
    """Verify that current contracts are valid JSON and can be loaded"""
    contract_dir = "contracts"
    for filename in os.listdir(contract_dir):
        if filename.endswith(".json"):
            path = os.path.join(contract_dir, filename)
            with open(path, "r") as f:
                data = json.load(f)
                assert isinstance(data, dict)
