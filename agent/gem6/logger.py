from typing import Dict, Any, List, Optional
import uuid
import json
import hashlib
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class AuditLogger:
    """
    Logging inmutable para auditoría y cumplimiento normativo (Compliance).
    Calcula checksums para garantizar la integridad de los logs.
    """
    
    def __init__(self, log_dir: str):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "audit_trail.jsonl")
        
    def log_event(self, level: str, pipeline_id: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Registra un evento de auditoría con integridad verificable."""
        entry = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': level,
            'pipeline_id': pipeline_id,
            'message': message,
            'metadata': metadata or {},
        }
        
        # Inyectar checksum antes de persistir
        entry['checksum'] = self._calculate_checksum(entry)
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

    def log_worker_error(self, worker_name: str, error: str, pipeline_id: str = "system"):
        self.log_event(
            level='ERROR',
            pipeline_id=pipeline_id,
            message=f"Critical error in worker {worker_name}",
            metadata={'worker': worker_name, 'error': error}
        )

    def _calculate_checksum(self, entry: Dict[str, Any]) -> str:
        # Serialización determinista para el hash
        data = json.dumps(entry, sort_keys=True, ensure_ascii=False).encode()
        return hashlib.sha256(data).hexdigest()

    def verify_integrity(self) -> bool:
        """Verifica que ningún log haya sido alterado manualmente."""
        if not os.path.exists(self.log_file):
            return True
            
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line)
                    stored_checksum = entry.pop('checksum', None)
                    if not stored_checksum:
                        return False
                    if self._calculate_checksum(entry) != stored_checksum:
                        return False
            return True
        except Exception:
            return False
