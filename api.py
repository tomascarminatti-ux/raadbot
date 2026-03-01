import os
import json
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import asyncio

import config
from agent.gemini_client import GeminiClient
from agent.gem6.orchestrator import GEM6Orchestrator
from agent.drive_client import DriveClient
from utils.input_loader import load_local_inputs
from utils.ws_logger import active_connections


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
    version="3.0.0",
    lifespan=lifespan,
)

# --- Configuración de CORS ---
# Permite que la frontend de Netlify y el dashboard local se comuniquen con la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://raadbot.netlify.app",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


async def run_pipeline(request: PipelineRequest) -> dict:
    """Wrapper asíncrono para ejecutar el pipeline completo usando GEM 6."""
    api_key = config.GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY no configurada.")

    if not request.drive_folder and not request.local_dir:
        raise ValueError("Se debe proveer 'drive_folder' o 'local_dir'.")

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

    # Ejecución asíncrona no bloqueante
    await orchestrator.run_pipeline(search_inputs, candidates)

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
        resultado = await run_pipeline(request)
        if request.webhook_url:
            async with httpx.AsyncClient() as client:
                await client.post(request.webhook_url, json=resultado, timeout=60.0)
    except Exception as e:
        if request.webhook_url:
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(
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
        try:
            return await run_pipeline(request)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


class SetupSearchRequest(BaseModel):
    search_id: str
    brief_notes: str
    jd_content: str
    company_context: Optional[str] = None

@app.post("/api/v1/search/setup")
async def setup_search(request: SetupSearchRequest):
    """
    Inicializa una búsqueda ejecutando únicamente GEM 5 (Radiografía Estratégica).
    Crea la estructura de carpetas y guarda el mandato inicial.
    """
    output_dir = os.path.join("runs", request.search_id, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    # Simular estructura de inputs para GEM 5
    search_inputs = {
        "kickoff_notes": request.brief_notes,
        "brief_jd": request.jd_content,
        "company_context": request.company_context or ""
    }
    
    gemini = GeminiClient(api_key=config.GEMINI_API_KEY)
    # Ejecutar GEM 5 directamente
    from agent.prompt_builder import build_gem5_prompt
    prompt = build_gem5_prompt(search_inputs)
    result = gemini.run_gem(prompt, gem_name="gem5")
    
    # Guardar resultados
    with open(os.path.join(output_dir, "gem5.json"), "w", encoding="utf-8") as f:
        json.dump(result.get("data", {}), f, indent=4)
    with open(os.path.join(output_dir, "gem5.md"), "w", encoding="utf-8") as f:
        f.write(result.get("markdown", ""))
        
    return {
        "status": "success",
        "search_id": request.search_id,
        "gem5_summary": result.get("data", {}).get("mandate_summary", "Mandato generado con éxito.")
    }


# --- Dashboard Endpoints ---

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    """Sirve la interfaz del Dashboard."""
    try:
        with open("templates/dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Dashboard template not found. Please create templates/dashboard.html"

@app.get("/api/v1/gems")
async def list_gems():
    """Lista metadatos y prompts actuales de los GEMs."""
    gems = []
    gem_list = ["gem1", "gem2", "gem3", "gem4", "gem5"]
    
    for g in gem_list:
        prompt_path = f"prompts/{g}.md"
        prompt_content = ""
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_content = f.read()
        
        gems.append({
            "id": g,
            "name": g.upper(),
            "prompt": prompt_content,
            "config": config.GEM_CONFIGS.get(g, {})
        })
    
    return gems

class RefineRequest(BaseModel):
    gem_id: str
    instruction: str

@app.post("/api/v1/gems/refine")
async def refine_gem(request: RefineRequest):
    """Refina un prompt GEM usando IA basado en una instrucción del usuario."""
    prompt_path = f"prompts/{request.gem_id}.md"
    if not os.path.exists(prompt_path):
        raise HTTPException(status_code=404, detail="GEM prompt file not found")
        
    with open(prompt_path, "r", encoding="utf-8") as f:
        current_prompt = f.read()
        
    refinement_prompt = f"""
    Eres un experto en Prompt Engineering. Tu misión es REFINAR el siguiente System Prompt de RAADBOT v2.0.
    
    ESTRUCTURA ACTUAL:
    {current_prompt}
    
    INSTRUCCIÓN DEL USUARIO:
    {request.instruction}
    
    REGLAS:
    1. Mantén la estructura de secciones (ROL, CONTEXTO, INSTRUCCIONES CORE, etc.).
    2. Aplica la instrucción del usuario de forma profesional y precisa.
    3. Devuelve el prompt REFINADO completo en formato Markdown.
    4. NO agregues explicaciones, solo el contenido del nuevo prompt.
    """
    
    gemini = GeminiClient(api_key=config.GEMINI_API_KEY)
    result = gemini.run_gem(refinement_prompt)
    new_prompt = result.get("markdown", "") or result.get("raw", "")
    
    if new_prompt:
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(new_prompt)
        # Invalida el cache para asegurar que el nuevo prompt se cargue
        from agent.prompt_builder import load_prompt
        load_prompt.cache_clear()
        return {"status": "success", "new_prompt": new_prompt}
    
    return {"status": "error", "message": "Failed to generate new prompt"}

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keep connection alive
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)

@app.get("/health")
def health_check():
    return {
        "status": "ok", 
        "agent": "raadbot", 
        "version": "3.0.0",
        "model": config.DEFAULT_MODEL,
        "provider": config.LLM_PROVIDER
    }
