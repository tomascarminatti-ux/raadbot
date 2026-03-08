import asyncio
import os
import sys
from datetime import datetime, timezone

# Asegurar que el path incluya la raíz del proyecto
sys.path.append(os.getcwd())

from agent.gemini_client import GeminiClient
from agent.gem6.orchestrator import GEM6Orchestrator

async def test_gem6_flow():
    print("🚀 Iniciando Test GEM 6 - Master Orchestrator...")
    
    # Configuración Mock
    api_key = os.getenv("GEMINI_API_KEY", "dummy_key")
    gemini = GeminiClient(api_key=api_key)
    output_dir = "runs/test_gem6"
    config_dict = {"search_id": "TEST-SEARCH-001"}
    
    orchestrator = GEM6Orchestrator(gemini, output_dir, config_dict)
    
    # Inputs Mock
    search_inputs = {"perfil": "CTO para Startup Fintech", "empresa": "RaadAdvisory"}
    candidates = {
        "CAND-001": {
            "cv_text": "Experiencia liderando equipos de ingeniería...",
            "interview_notes": "Muy técnico, buen fit cultural."
        }
    }
    
    try:
        # Nota: En un test real sin API Key de verdad, gemini.run_gem fallará o devolverá error.
        # Aquí probamos la estructura de la orquestación.
        # El método es run_pipeline, no execute_pipeline
        result = await orchestrator.run_pipeline(search_inputs, candidates)
        
        print("\n✅ Pipeline Ejecutado!")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"\n❌ Error en el test: {e}")

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Aviso: No hay GEMINI_API_KEY. El test ejecutará la lógica pero las llamadas a la API fallarán.")
    asyncio.run(test_gem6_flow())
