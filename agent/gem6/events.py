import asyncio
import uuid
import json
import logging
from typing import Dict, List, Callable, Any, Awaitable
from datetime import datetime, timezone
from collections import defaultdict

logger = logging.getLogger(__name__)

class EventBus:
    """
    Sistema de eventos para comunicación asíncrona entre componentes del pipeline GEM 6.
    """
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Dict[str, Any]], Awaitable[None]]]] = defaultdict(list)
        self.event_store: List[Dict[str, Any]] = []
        
    async def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], Awaitable[None]]):
        """
        Suscribe un handler a un tipo de evento.
        """
        self.subscribers[event_type].append(handler)
        
    async def publish(self, event_type: str, payload: Dict[str, Any]):
        """
        Publica un evento a todos los suscriptores interesados.
        """
        event = {
            'id': str(uuid.uuid4()),
            'type': event_type,
            'payload': payload,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        # Persistencia en memoria para auditoría inmediata
        self.event_store.append(event)
        
        logger.debug(f"Event Published: {event_type} - {event['id']}")
        
        # Notificar suscriptores de forma asíncrona
        tasks = []
        for handler in self.subscribers.get(event_type, []):
            tasks.append(asyncio.create_task(self._safe_call_handler(handler, event)))
        
        # También notificar a los suscriptores globales '*'
        for handler in self.subscribers.get('*', []):
            tasks.append(asyncio.create_task(self._safe_call_handler(handler, event)))
            
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_call_handler(self, handler: Callable, event: Dict[str, Any]):
        try:
            await handler(event)
        except Exception as e:
            logger.error(f"Error in EventBus handler for {event['type']}: {e}", exc_info=True)
                
    def get_event_history(self, pipeline_id: str = "") -> List[Dict[str, Any]]:
        """
        Recupera historial de eventos, opcionalmente filtrado por pipeline_id.
        """
        if not pipeline_id:
            return self.event_store
            
        return [e for e in self.event_store 
                if e['payload'].get('pipeline_id') == pipeline_id]
