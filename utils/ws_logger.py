import asyncio
import json
import os
import threading
from datetime import datetime
from typing import List, Optional
from fastapi import WebSocket

active_connections: List[WebSocket] = []
_steps_cache: Optional[List[dict]] = None
_write_lock = threading.Lock()

def _write_state(steps: List[dict]):
    """Sync helper to write state to disk without blocking the event loop."""
    # Ensure only one thread writes at a time to prevent file corruption
    with _write_lock:
        try:
            with open("pipeline_state.json", "w", encoding="utf-8") as f:
                json.dump({"steps": steps}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error updating pipeline_state.json: {e}")

async def broadcast_log(data: dict):
    """
    Broadcasts a log message to all connected WebSocket clients.
    Uses an in-memory cache and background threads to avoid redundant disk I/O.
    """
    global _steps_cache
    message = {
        "timestamp": datetime.now().isoformat(),
        **data
    }

    # Send to WebSockets
    for connection in active_connections[:]:
        try:
            await connection.send_json(message)
        except Exception:
            if connection in active_connections:
                active_connections.remove(connection)

    # Initialize cache from disk on first call
    if _steps_cache is None:
        try:
            if os.path.exists("pipeline_state.json"):
                with open("pipeline_state.json", "r", encoding="utf-8") as f:
                    state = json.load(f)
                    _steps_cache = state.get("steps", [])
            else:
                _steps_cache = []
        except (FileNotFoundError, json.JSONDecodeError):
            _steps_cache = []

    # Update memory state
    _steps_cache.append(message)
    _steps_cache = _steps_cache[-50:]

    # Offload blocking disk write to a background thread
    # We pass a copy of the list to avoid mutations during JSON serialization
    asyncio.create_task(asyncio.to_thread(_write_state, list(_steps_cache)))
