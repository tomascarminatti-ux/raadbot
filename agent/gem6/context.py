from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import uuid
import json

class CandidateContext:
    def __init__(self, candidato_id: str, global_context: Dict[str, Any]):
        self.candidato_id = candidato_id
        self.global_context = global_context
        self.retry_counts = {'gem1': 0, 'gem2': 0, 'gem3': 0, 'gem4': 0}
        self.outputs = {'gem1': None, 'gem2': None, 'gem3': None, 'gem4': None}
        self.start_time = datetime.now(timezone.utc)
        self.events = []

    def increment_retry_count(self, gem_name: str):
        self.retry_counts[gem_name] = self.retry_counts.get(gem_name, 0) + 1

    def get_retry_count(self, gem_name: str, default: int = 0) -> int:
        return self.retry_counts.get(gem_name, default)

    def get_elapsed_seconds(self) -> float:
        return (datetime.now(timezone.utc) - self.start_time).total_seconds()

    def set_output(self, gem_name: str, output: Any):
        self.outputs[gem_name] = output

    def to_dict(self) -> Dict[str, Any]:
        return {
            'candidato_id': self.candidato_id,
            'retry_counts': self.retry_counts,
            'elapsed_seconds': self.get_elapsed_seconds(),
            'outputs': self.outputs
        }

class ContextManager:
    """
    Gestiona el estado global y contexto compartido entre GEMs.
    """
    
    def __init__(self):
        self.global_context = {}
        self.candidate_contexts: Dict[str, CandidateContext] = {}
        self.version_history = []
        
    def set_global_context(self, pipeline_id: str, mandato: dict, start_time: datetime):
        """
        Establece contexto global inmutable para una ejecución.
        """
        self.global_context = {
            'pipeline_id': pipeline_id,
            'mandato': mandato,
            'start_time': start_time,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'version': 1
        }
        
    def create_candidate_context(self, candidato_id: str) -> CandidateContext:
        """
        Crea un contexto aislado por cada candidato.
        """
        context = CandidateContext(
            candidato_id=candidato_id,
            global_context=self.global_context
        )
        self.candidate_contexts[candidato_id] = context
        return context
    
    def get_candidate_context(self, candidato_id: str) -> Optional[CandidateContext]:
        return self.candidate_contexts.get(candidato_id)

    def get_elapsed_seconds(self) -> float:
        """
        Calcula tiempo transcurrido desde el inicio global.
        """
        if not self.global_context:
            return 0.0
        start = self.global_context['start_time']
        return (datetime.now(timezone.utc) - start).total_seconds()
