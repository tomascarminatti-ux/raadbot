import os
import json
from contextlib import asynccontextmanager
from typing import Optional
import httpx

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv

# Ensure environment is loaded
load_dotenv()

from agent.gemini_client import GeminiClient
from agent.pipeline import Pipeline
from agent.drive_client import DriveClient
from agent.utils import load_local_inputs
from agent.config import DEFAULT_MODEL
from agent.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Check for API Key on startup
    if not os.getenv("GEMINI_API_KEY"):
        logger.warning(
            "⚠️  WARNING: GEMINI_API_KEY no detectada. La API fallará si no se configura al momento del request."
        )
    yield


app = FastAPI(
    title="Raadbot API",
    description="API interna para integrar Raadbot con n8n u otros sistemas externos.",
    version="1.0.0",
    lifespan=lifespan,
)


class PipelineRequest(BaseModel):
    search_id: str
    drive_folder: Optional[str] = None
    local_dir: Optional[str] = None
    candidate_id: Optional[str] = None  # Si se quiere procesar solo uno
    model: str = DEFAULT_MODEL
    webhook_url: Optional[str] = None  # Para n8n asíncrono


class PipelineResponse(BaseModel):
    status: str
    search_id: str
    output_dir: str
    summary: dict


async def run_pipeline_logic(request: PipelineRequest) -> dict:
    """Lógica central para ejecutar el pipeline completo (async)."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY no configurada en las variables de entorno.")

    if not request.drive_folder and not request.local_dir:
        raise ValueError("Se debe proveer 'drive_folder' o 'local_dir'.")

    search_inputs = {}
    candidates = {}

    if request.drive_folder:
        try:
            drive = DriveClient()
            structure = drive.discover_search_structure(request.drive_folder)
            search_inputs = structure["search_inputs"]
            candidates = structure["candidates"]
        except Exception as e:
            raise ValueError(f"Error de sincronización con Google Drive: {str(e)}")
    else:
        try:
            search_inputs, candidates = load_local_inputs(request.local_dir)
        except Exception as e:
            raise ValueError(
                f"Error cargando directorio local {request.local_dir}: {str(e)}"
            )

    if request.candidate_id:
        if request.candidate_id not in candidates:
            raise ValueError(f"Candidato {request.candidate_id} no encontrado.")
        candidates = {request.candidate_id: candidates[request.candidate_id]}

    output_dir = os.path.join("runs", request.search_id, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    gemini = GeminiClient(api_key=api_key, model=request.model)
    pipeline = Pipeline(
        gemini=gemini, search_id=request.search_id, output_dir=output_dir
    )

    results = await pipeline.run_full_pipeline(search_inputs, candidates)

    # Load the pipeline_summary.json to return it to the caller
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


async def background_run_pipeline(request: PipelineRequest):
    """Ejecuta el pipeline de fondo y llama a un webhook si existe."""
    try:
        resultado = await run_pipeline_logic(request)
        if request.webhook_url:
            async with httpx.AsyncClient() as client:
                await client.post(request.webhook_url, json=resultado, timeout=30.0)
    except Exception as e:
        if request.webhook_url:
            async with httpx.AsyncClient() as client:
                await client.post(
                    request.webhook_url,
                    json={"status": "error", "message": str(e)},
                    timeout=30.0,
                )


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
        try:
            return await run_pipeline_logic(request)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok", "agent": "raadbot"}
