from typing import List
import asyncio
import json
import os
from datetime import datetime
from fastapi import WebSocket

active_connections: List[WebSocket] = []
state_lock = asyncio.Lock()


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
    async with state_lock:
        try:
            state_file = "pipeline_state.json"
            state = {"steps": []}
            try:
                # Use to_thread for blocking file I/O to avoid blocking event loop
                def read_state():
                    if os.path.exists(state_file):
                        with open(state_file, "r", encoding="utf-8") as f:
                            return json.load(f)
                    return {"steps": []}

                state = await asyncio.to_thread(read_state)
            except (FileNotFoundError, json.JSONDecodeError):
                pass

            state["steps"].append(message)
            # Keep only last 50 steps to avoid file bloat
            state["steps"] = state["steps"][-50:]

            def write_state(data):
                with open(state_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

            await asyncio.to_thread(write_state, state)
        except Exception as e:
            print(f"Error updating pipeline_state.json: {e}")
