import httpx
import json
import logging
from typing import Dict, Any, Optional

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
    """Client for DB interactions with connection pooling."""
    def __init__(self, db_url: str = "http://db-api:8000"):
        self.db_url = db_url
        # Optimization: use a persistent client for connection pooling
        self._client = httpx.AsyncClient(timeout=30.0)

    async def aclose(self):
        """Close the underlying httpx client."""
        await self._client.aclose()

    async def _post(self, endpoint: str, data: Dict[str, Any]):
        """Internal helper for POST requests."""
        try:
            resp = await self._client.post(f"{self.db_url}{endpoint}", json=data)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"DB API error on {endpoint}: {e}")
            return None

    async def upsert_entity(self, data: Dict[str, Any]):
        return await self._post("/entity/upsert", data)

    async def discard_entity(self, data: Dict[str, Any]):
        return await self._post("/entity/discard", data)

    async def log_execution(self, log_data: Dict[str, Any]):
        return await self._post("/log/discovery", log_data)

def validate_contract(data: Dict[str, Any], contract_path: str) -> bool:
    try:
        with open(contract_path, "r") as f:
            contract = json.load(f)
        
        for key in contract:
            if not isinstance(key, str):
                continue
            expected_type = contract[key]
            if key not in data:
                logger.warning(f"Contract Violation: Missing key '{key}'")
                return False
            # Basic type checking
            val = data.get(key)
            if expected_type == "array" and not isinstance(val, list): return False
            if expected_type == "number" and not isinstance(val, (int, float)): return False
            if expected_type == "string" and not isinstance(val, str): return False
            if expected_type == "object" and not isinstance(val, dict): return False
            if expected_type == "boolean" and not isinstance(val, bool): return False
            
        return True
    except Exception as e:
        logger.error(f"Contract validation error: {e}")
        return False
