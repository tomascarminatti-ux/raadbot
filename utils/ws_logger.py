import asyncio
import json
from datetime import datetime
from typing import List
from fastapi import WebSocket

active_connections: List[WebSocket] = []
_pipeline_lock = None

def get_pipeline_lock():
    global _pipeline_lock
    if _pipeline_lock is None:
        _pipeline_lock = asyncio.Lock()
    return _pipeline_lock

async def broadcast_log(data: dict):
    """
    Broadcasts a log message to all connected WebSocket clients.
    Also saves the latest state to pipeline_state.json for Streamlit.
    """
    message = {
        "timestamp": datetime.now().isoformat(),
        **data
    }

    # Send to WebSockets
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception:
            disconnected.append(connection)

    for d in disconnected:
        if d in active_connections:
            active_connections.remove(d)

    # Update pipeline_state.json for Streamlit compatibility (Thread-safe & Non-blocking)
    lock = get_pipeline_lock()
    async with lock:
        try:
            await asyncio.to_thread(_update_pipeline_state, message)
        except Exception as e:
            print(f"Error updating pipeline_state.json: {e}")

def _update_pipeline_state(message: dict):
    """Synchronous helper to update the pipeline state file."""
    state_file = "pipeline_state.json"
    state = {"steps": []}
    try:
        if json_content := open(state_file, "r", encoding="utf-8").read():
            state = json.loads(json_content)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    state.setdefault("steps", []).append(message)
    # Keep only last 50 steps to avoid file bloat
    state["steps"] = state["steps"][-50:]

    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
