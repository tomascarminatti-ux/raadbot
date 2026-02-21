import os
import json
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import httpx

import config
from agent.gemini_client import GeminiClient
from agent.gem6.orchestrator import GEM6Orchestrator
from agent.drive_client import DriveClient
from utils.input_loader import load_local_inputs


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Check for API Key on startup
    if not config.GEMINI_API_KEY:
        print(
            "⚠️  WARNING: GEMINI_API_KEY no detectada. La API fallará si no se configura al momento del request."
        )
    yield


app = FastAPI(
    title="Raadbot API",
    description="API interna para integrar Raadbot con n8n u otros sistemas externos.",
    version="2.0.0",
    lifespan=lifespan,
)


class PipelineRequest(BaseModel):
    search_id: str
    drive_folder: Optional[str] = None
    local_dir: Optional[str] = None
    candidate_id: Optional[str] = None  # Si se quiere procesar solo uno
    model: str = config.DEFAULT_MODEL
    webhook_url: Optional[str] = None  # Para n8n asíncrono


class PipelineResponse(BaseModel):
    status: str
    search_id: str
    output_dir: str
    summary: dict


def run_pipeline_sync(request: PipelineRequest) -> dict:
    """Wrapper síncrono para ejecutar el pipeline completo usando GEM 6."""
    api_key = config.GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY no configurada.")

    if not request.drive_folder and not request.local_dir:
        raise ValueError("Se debe proveer 'drive_folder' o 'local_dir'.")

    # Load inputs (omitted identical logic for brevity in replace, but keeping it in the actual file)
    search_inputs = {}
    candidates = {}

    if request.drive_folder:
        drive = DriveClient(credentials_path=config.DRIVE_CREDENTIALS_PATH)
        structure = drive.discover_search_structure(request.drive_folder)
        search_inputs = structure["search_inputs"]
        candidates = structure["candidates"]
    else:
        search_inputs, candidates = load_local_inputs(request.local_dir)

    if request.candidate_id:
        if request.candidate_id not in candidates:
            raise ValueError(f"Candidato {request.candidate_id} no encontrado.")
        candidates = {request.candidate_id: candidates[request.candidate_id]}

    output_dir = os.path.join("runs", request.search_id, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    gemini = GeminiClient(api_key=api_key, model=request.model)
    orchestrator = GEM6Orchestrator(gemini=gemini, search_id=request.search_id, output_dir=output_dir)

    import asyncio
    # Ejecución bloqueante para el worker actual
    asyncio.run(orchestrator.run_pipeline(search_inputs, candidates))

    summary_path = os.path.join(output_dir, "pipeline_summary.json")
    summary_data = {}
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            summary_data = json.load(f)

    return {
        "status": "success",
        "search_id": request.search_id,
        "output_dir": output_dir,
        "summary": summary_data,
    }


def background_run_pipeline(request: PipelineRequest):
    """Ejecuta el pipeline de fondo y llama a un webhook si existe."""
    try:
        resultado = run_pipeline_sync(request)
        if request.webhook_url:
            httpx.post(request.webhook_url, json=resultado, timeout=60.0)
    except Exception as e:
        if request.webhook_url:
            try:
                httpx.post(
                    request.webhook_url,
                    json={
                        "status": "error", 
                        "search_id": request.search_id, 
                        "message": str(e)
                    },
                    timeout=30.0,
                )
            except Exception:
                pass


@app.post("/api/v1/run")
async def trigger_pipeline(request: PipelineRequest, background_tasks: BackgroundTasks):
    """
    Verbo POST para iniciar una corrida del pipeline.
    Soporta webhook_url para ejecuciones asíncronas no bloqueantes.
    """
    if request.webhook_url:
        background_tasks.add_task(background_run_pipeline, request)
        return {
            "status": "processing",
            "message": "Pipeline iniciado de fondo.",
            "search_id": request.search_id,
        }
    else:
        # Nota: Esto sigue siendo bloqueante para el worker de FastAPI. 
        # En producción se recomienda usar siempre el modo asíncrono con webhooks.
        try:
            return run_pipeline_sync(request)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health_check():
    return {
        "status": "ok", 
        "agent": "raadbot", 
        "version": "2.0.0",
        "model": config.DEFAULT_MODEL
    }
