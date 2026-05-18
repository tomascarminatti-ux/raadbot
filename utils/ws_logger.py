import asyncio
import json
import os
import threading
from datetime import datetime
from typing import List
from fastapi import WebSocket

active_connections: List[WebSocket] = []

# Global cache and lock for thread-safe state management
_state_lock = threading.Lock()
_pipeline_state_steps = []
_STATE_FILE = "pipeline_state.json"

# Initialize state from disk if it exists
if os.path.exists(_STATE_FILE):
    try:
        with open(_STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            _pipeline_state_steps = data.get("steps", [])
    except (json.JSONDecodeError, Exception):
        _pipeline_state_steps = []

def _sync_save_state(steps_snapshot: list):
    """Saves the state snapshot to disk."""
    try:
        state_data = {"steps": steps_snapshot}
        with open(_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving {_STATE_FILE}: {e}")

async def broadcast_log(data: dict):
    """
    Broadcasts a log message to all connected WebSocket clients.
    Also updates the in-memory state and persists it to disk in the background.
    """
    message = {
        "timestamp": datetime.now().isoformat(),
        **data
    }

    # 1. Send to WebSockets (Async)
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception:
            disconnected.append(connection)

    for d in disconnected:
        if d in active_connections:
            try:
                active_connections.remove(d)
            except ValueError:
                pass

    # 2. Update In-Memory Cache and take a thread-safe snapshot for disk write
    with _state_lock:
        _pipeline_state_steps.append(message)
        # Keep only last 50 steps
        if len(_pipeline_state_steps) > 50:
            _pipeline_state_steps[:] = _pipeline_state_steps[-50:]

        # Take a snapshot of the list to avoid RuntimeError in the background thread
        # if the main thread modifies the list during JSON serialization.
        steps_snapshot = list(_pipeline_state_steps)

    # 3. Background Disk Write (Non-blocking)
    # Offload blocking I/O and JSON serialization to a thread pool
    asyncio.create_task(asyncio.to_thread(_sync_save_state, steps_snapshot))
