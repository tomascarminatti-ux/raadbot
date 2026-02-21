from typing import Dict, List, Tuple, Callable, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GEM6StateMachine:
    """
    Controla las transiciones entre estados del pipeline GEM 6.
    Inspirado en la especificación técnica industrial.
    """
    
    STATES = {
        'INITIALIZED': 'Pipeline creado, validando inputs',
        'GEM5_VALIDATED': 'GEM 5 completado y aprobado',
        'PROCESSING_CANDIDATES': 'Iterando sobre candidatos',
        'GEM1_RUNNING': 'GEM 1 en ejecución',
        'GEM2_RUNNING': 'GEM 2 en ejecución',
        'GEM1_GEM2_SYNC': 'Esperando completitud de ambos',
        'EVALUATING_SCORES': 'Validando scores contra umbrales',
        'DISCARDED': 'Candidato descartado (score < umbral)',
        'GEM3_RUNNING': 'GEM 3 en ejecución',
        'GEM4_RUNNING': 'GEM 4 en ejecución',
        'QA_PASSED': 'GEM 4 aprobó (score >= 7)',
        'QA_FAILED_RETRY': 'GEM 4 falló, reintentando',
        'QA_FAILED_ESCALATE': 'GEM 4 falló, escalando a humano',
        'COMPLETED': 'Pipeline completado exitosamente',
        'FAILED': 'Pipeline falló (error no recuperable)',
        'TIMEOUT': 'Pipeline excedió SLA'
    }
    
    def __init__(self, initial_state: str = 'INITIALIZED'):
        if initial_state not in self.STATES:
            raise ValueError(f"Estado inicial inválido: {initial_state}")
        self._current_state = initial_state
        self._transitions: List[Tuple[str, str, str, Optional[Callable]]] = []
        self._setup_transitions()

    def _setup_transitions(self):
        # (from_state, event, to_state, action)
        self.add_transition('INITIALIZED', 'validate_gem5', 'GEM5_VALIDATED')
        self.add_transition('GEM5_VALIDATED', 'start_candidates', 'PROCESSING_CANDIDATES')
        self.add_transition('PROCESSING_CANDIDATES', 'dispatch_gem1_gem2', 'GEM1_GEM2_SYNC')
        self.add_transition('GEM1_GEM2_SYNC', 'both_completed', 'EVALUATING_SCORES')
        self.add_transition('EVALUATING_SCORES', 'scores_below_threshold', 'DISCARDED')
        self.add_transition('EVALUATING_SCORES', 'scores_above_threshold', 'GEM3_RUNNING')
        self.add_transition('GEM3_RUNNING', 'gem3_completed', 'GEM4_RUNNING')
        self.add_transition('GEM4_RUNNING', 'gem4_score_ge_7', 'QA_PASSED')
        self.add_transition('GEM4_RUNNING', 'gem4_score_lt_7_retry', 'QA_FAILED_RETRY')
        self.add_transition('GEM4_RUNNING', 'gem4_score_lt_7_escalate', 'QA_FAILED_ESCALATE')
        self.add_transition('QA_PASSED', 'all_candidates_done', 'COMPLETED')
        
        # Transiciones globales
        # Usamos '*' para denotar que puede venir de cualquier estado
        self.add_transition('*', 'timeout_exceeded', 'TIMEOUT')
        self.add_transition('*', 'critical_error', 'FAILED')

    def add_transition(self, from_state: str, event: str, to_state: str, action: Optional[Callable] = None):
        self._transitions.append((from_state, event, to_state, action))

    @property
    def current_state(self) -> str:
        return self._current_state

    def transition(self, event: str, *args, **kwargs) -> bool:
        """
        Intenta realizar una transición de estado basada en un evento.
        """
        for from_state, evt, to_state, action in self._transitions:
            if (from_state == self._current_state or from_state == '*') and evt == event:
                old_state = self._current_state
                self._current_state = to_state
                
                logger.info(f"State Transition: {old_state} --({event})--> {to_state}")
                
                if action:
                    action(*args, **kwargs)
                return True
        
        logger.warning(f"Invalid Transition: No transition for event '{event}' from state '{self._current_state}'")
        return False
