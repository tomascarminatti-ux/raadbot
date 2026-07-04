import httpx
import json
import logging
import functools
from typing import Dict, Any


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

    async def upsert_entity(self, data: Dict[str, Any]):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.db_url}/entity/upsert", json=data)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error(f"Failed to upsert entity: {e}")
            return None

    async def discard_entity(self, data: Dict[str, Any]):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.db_url}/entity/discard", json=data)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error(f"Failed to discard entity: {e}")
            return None

    async def log_execution(self, log_data: Dict[str, Any]):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.db_url}/log/discovery", json=log_data)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error(f"Failed to log execution: {e}")
            return None


@functools.lru_cache(maxsize=32)
def _load_schema(contract_path: str) -> Dict[str, Any]:
    """Carga y cachea el esquema del contrato desde el disco."""
    with open(contract_path, "r") as f:
        return json.load(f)


def _check_type(val: Any, expected_type: str) -> bool:
    """Realiza la comprobación de tipos básica."""
    type_map = {
        "array": list,
        "number": (int, float),
        "string": str,
        "object": dict,
        "boolean": bool
    }
    target_type = type_map.get(expected_type)
    if target_type:
        return isinstance(val, target_type)
    return True


def validate_contract(data: Dict[str, Any], contract_path: str) -> bool:
    """Valida que los datos cumplan con el contrato definido en un archivo JSON."""
    try:
        contract = _load_schema(contract_path)

        for key, expected_type in contract.items():
            if not isinstance(key, str):
                continue
            if key not in data:
                logger.warning(f"Contract Violation: Missing key '{key}'")
                return False

            if not _check_type(data.get(key), expected_type):
                return False

        return True
    except Exception as e:
        logger.error(f"Contract validation error: {e}")
        return False
