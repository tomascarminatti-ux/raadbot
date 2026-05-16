import asyncio
import json
import os
import threading
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import WebSocket

active_connections: List[WebSocket] = []

# Bolt Optimization: Cache the pipeline state in memory to avoid repeated disk I/O
_state_cache: Optional[Dict[str, Any]] = None
STATE_FILE = "pipeline_state.json"
# Bolt Optimization: Thread-local lock for file writing to handle concurrency gracefully
_file_lock = threading.Lock()

def _save_state_to_disk(state: Dict[str, Any], identifier: str):
    """
    Synchronous helper to save state to disk with atomic write.
    """
    with _file_lock:
        try:
            temp_file = f"{STATE_FILE}.{identifier}.tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            os.replace(temp_file, STATE_FILE)
        except Exception as e:
            print(f"Error saving pipeline_state.json: {e}")

async def broadcast_log(data: dict):
    """
    Broadcasts a log message to all connected WebSocket clients.
    Also saves the latest state to pipeline_state.json for Streamlit.
    """
    global _state_cache

    message = {
        "timestamp": datetime.now().isoformat(),
        **data
    }

    # Send to WebSockets
    if active_connections:
        disconnected = []
        for connection in active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for d in disconnected:
            if d in active_connections:
                active_connections.remove(d)

    # Update pipeline_state.json for Streamlit compatibility
    # Bolt Optimization: Using in-memory cache and non-blocking background write
    try:
        if _state_cache is None:
            # First time: try to load from disk or initialize
            if os.path.exists(STATE_FILE):
                try:
                    with open(STATE_FILE, "r", encoding="utf-8") as f:
                        _state_cache = json.load(f)
                except (json.JSONDecodeError, IOError):
                    _state_cache = {"steps": []}
            else:
                _state_cache = {"steps": []}

        if "steps" not in _state_cache:
            _state_cache["steps"] = []

        _state_cache["steps"].append(message)
        # Keep only last 50 steps to avoid file bloat
        _state_cache["steps"] = _state_cache["steps"][-50:]

        # Bolt Optimization: Non-blocking write using asyncio.to_thread
        # We pass a snapshot of the current steps to avoid race conditions
        state_to_save = {"steps": list(_state_cache["steps"])}

        try:
            # Use a unique identifier for the temp file to avoid race conditions between threads
            write_id = str(uuid.uuid4())[:8]
            asyncio.create_task(asyncio.to_thread(_save_state_to_disk, state_to_save, write_id))
        except RuntimeError:
            # Fallback for environments without a running event loop
            _save_state_to_disk(state_to_save, "sync")

    except Exception as e:
        print(f"Error updating pipeline_state.json: {e}")
