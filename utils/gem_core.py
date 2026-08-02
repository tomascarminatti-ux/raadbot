import functools
import json
import logging
import os
from typing import Any

import httpx


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if hasattr(record, "extra_fields"):
            log_record.update(record.extra_fields)
        return json.dumps(log_record)


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("gem_v3")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False


class GEMClient:
    def __init__(self, db_url: str = "http://db-api:8000"):
        self.db_url = db_url

    async def upsert_entity(self, data: dict[str, Any]):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.db_url}/entity/upsert", json=data)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error(f"Failed to upsert entity: {e}")
            return None

    async def discard_entity(self, data: dict[str, Any]):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.db_url}/entity/discard", json=data)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error(f"Failed to discard entity: {e}")
            return None

    async def log_execution(self, log_data: dict[str, Any]):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.db_url}/log/discovery", json=log_data)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error(f"Failed to log execution: {e}")
            return None


@functools.lru_cache(maxsize=32)
def _load_contract_cached(contract_path: str, mtime: float) -> dict:
    """Helper interno con lru_cache para evitar lecturas de disco repetidas de esquemas de contratos."""
    with open(contract_path, "r") as f:
        return json.load(f)


def validate_contract(data: dict[str, Any], contract_path: str) -> bool:
    try:
        if not os.path.exists(contract_path):
            logger.warning(f"Contract schema not found: {contract_path}")
            return False

        mtime = os.path.getmtime(contract_path)
        contract = _load_contract_cached(contract_path, mtime)

        for key in contract:
            if not isinstance(key, str):
                continue
            expected_type = contract[key]
            if key not in data:
                logger.warning(f"Contract Violation: Missing key '{key}'")
                return False
            # Basic type checking
            val = data.get(key)
            if expected_type == "array" and not isinstance(val, list):
                return False
            if expected_type == "number" and not isinstance(val, (int, float)):
                return False
            if expected_type == "string" and not isinstance(val, str):
                return False
            if expected_type == "object" and not isinstance(val, dict):
                return False
            if expected_type == "boolean" and not isinstance(val, bool):
                return False

        return True
    except Exception as e:
        logger.error(f"Contract validation error: {e}")
        return False
