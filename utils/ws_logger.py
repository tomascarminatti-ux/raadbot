import asyncio
import json
import os
from datetime import datetime
from typing import List
from fastapi import WebSocket

active_connections: List[WebSocket] = []
_log_queue: asyncio.Queue = asyncio.Queue()
_worker_started = False


async def _file_writer_task():
    """Background task to persist logs to disk without blocking the main loop."""
    state_file = "pipeline_state.json"
    state = {"steps": []}

    # Initial load of existing state
    try:
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    while True:
        message = await _log_queue.get()
        state["steps"].append(message)
        state["steps"] = state["steps"][-50:]

        try:
            # Perform blocking I/O in a separate thread to keep event loop responsive
            def save_to_disk():
                with open(state_file, "w", encoding="utf-8") as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)
            await asyncio.to_thread(save_to_disk)
        except Exception as e:
            print(f"[ws_logger] Error updating pipeline_state.json: {e}")
        finally:
            _log_queue.task_done()


async def broadcast_log(data: dict):
    """
    Broadcasts a log message to all connected WebSocket clients immediately
    and queues it for background persistence to pipeline_state.json.
    """
    global _worker_started
    message = {
        "timestamp": datetime.now().isoformat(),
        **data
    }

    # Start the background worker if not already running
    if not _worker_started:
        asyncio.create_task(_file_writer_task())
        _worker_started = True

    # Send to WebSockets (immediate feedback)
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception:
            disconnected.append(connection)

    for d in disconnected:
        if d in active_connections:
            active_connections.remove(d)

    # Offload file persistence to the background queue
    await _log_queue.put(message)
