import os
import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="GEM v3.0 DB API")

DB_PATH = os.getenv("DB_PATH", "infra/db/gem_v3.sqlite")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    schema_path = "infra/db/schema.sql"
    if os.path.exists(schema_path):
        with open(schema_path, "r") as f:
            schema = f.read()
        conn = get_db()
        conn.executescript(schema)
        conn.commit()
        conn.close()


@app.on_event("startup")
def startup_event():
    init_db()

# Models


class EntityUpdate(BaseModel):
    entity_id: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")
    current_stage: str
    state: str
    last_score: Optional[float] = None
    human_required: Optional[bool] = False
    metadata: Optional[Dict[str, Any]] = {}
    agent_responsible: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")
    trace_id: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")


class DiscardEntity(BaseModel):
    entity_id: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")
    stage_at_discard: str
    reason: str
    score_at_discard: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = {}
    agent_responsible: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")
    trace_id: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")


class DiscoveryLog(BaseModel):
    entity_id: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")
    agent_id: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")
    input_ok: Optional[bool] = Field(None, alias="input_contract_verified")
    output_ok: Optional[bool] = Field(None, alias="output_contract_verified")
    time_ms: Optional[int] = Field(None, alias="execution_time_ms")
    status: Optional[str] = None
    error: Optional[str] = Field(None, alias="error_message")
    trace_id: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")

    class Config:
        populate_by_name = True

# Endpoints


@app.post("/entity/upsert")
async def upsert_entity(data: EntityUpdate):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    try:
        cursor.execute("""
            INSERT INTO entity_state (
                entity_id, current_stage, state, last_score,
                human_required, metadata, agent_responsible, trace_id,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entity_id) DO UPDATE SET
                current_stage=excluded.current_stage,
                state=excluded.state,
                last_score=excluded.last_score,
                human_required=excluded.human_required,
                metadata=excluded.metadata,
                agent_responsible=excluded.agent_responsible,
                trace_id=excluded.trace_id,
                updated_at=excluded.updated_at
        """, (
            data.entity_id, data.current_stage, data.state, data.last_score,
            data.human_required, json.dumps(
                data.metadata), data.agent_responsible, data.trace_id,
            now, now
        ))
        conn.commit()
        return {"status": "success"}
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal database error")
    finally:
        conn.close()


@app.post("/entity/discard")
async def discard_entity(data: DiscardEntity):
    conn = get_db()
    cursor = conn.cursor()

    try:
        # Move to discarded table
        cursor.execute("""
            INSERT INTO discarded_entities (
                entity_id, stage_at_discard, reason, score_at_discard,
                metadata, agent_responsible, trace_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.entity_id, data.stage_at_discard, data.reason, data.score_at_discard,
            json.dumps(data.metadata), data.agent_responsible, data.trace_id
        ))
        # Remove from active state
        cursor.execute(
            "DELETE FROM entity_state WHERE entity_id = ?", (data.entity_id,))
        conn.commit()
        return {"status": "discarded"}
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal database error")
    finally:
        conn.close()


@app.get("/entities")
async def get_entities(stage: Optional[str] = None):
    conn = get_db()
    cursor = conn.cursor()
    if stage:
        cursor.execute(
            "SELECT * FROM entity_state WHERE current_stage = ?", (stage,))
    else:
        cursor.execute("SELECT * FROM entity_state")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.post("/log/discovery")
async def log_discovery(data: DiscoveryLog):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO discovery_logs (
                entity_id, agent_id, input_contract_verified,
                output_contract_verified, execution_time_ms, status,
                error_message, trace_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.entity_id, data.agent_id, data.input_ok,
            data.output_ok, data.time_ms, data.status,
            data.error, data.trace_id
        ))
        conn.commit()
        return {"status": "logged"}
    finally:
        conn.close()


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "db-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
