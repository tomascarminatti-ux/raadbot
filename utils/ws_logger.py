import asyncio
import json
import os
from datetime import datetime
from typing import List, Optional
from fastapi import WebSocket

active_connections: List[WebSocket] = []
state_lock: Optional[asyncio.Lock] = None


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

    # Update pipeline_state.json for Streamlit compatibility
    # Use lock and to_thread to ensure thread-safety and non-blocking I/O
    global state_lock
    if state_lock is None:
        state_lock = asyncio.Lock()

    async with state_lock:
        try:
            state_file = "pipeline_state.json"

            def update_file():
                state = {"steps": []}
                try:
                    if os.path.exists(state_file):
                        with open(state_file, "r", encoding="utf-8") as f:
                            state = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    pass

                state["steps"].append(message)
                # Keep only last 50 steps to avoid file bloat
                state["steps"] = state["steps"][-50:]

                with open(state_file, "w", encoding="utf-8") as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)

            await asyncio.to_thread(update_file)
        except Exception as e:
            print(f"Error updating pipeline_state.json: {e}")
