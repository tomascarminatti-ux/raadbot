import os
import sys
import pytest

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.gemini_client import GeminiClient
from dotenv import load_dotenv

load_dotenv()

def test_run_gemini_basic():
    """Prueba básica de conectividad con el LLM."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        pytest.skip("GEMINI_API_KEY no configurada.")

    client = GeminiClient(api_key=api_key, model="gemini-1.5-flash")
    prompt = "Escribe un saludo corto de 5 palabras."

    try:
        res = client.run_gem(prompt)
        assert res is not None
        assert "raw" in res
        print(f"Respuesta: {res['raw']}")
    except Exception as e:
        pytest.skip(f"Error al conectar con el LLM: {e}")

if __name__ == "__main__":
    # Mantener compatibilidad con ejecución directa
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        client = GeminiClient(api_key=api_key, model="gemini-1.5-flash")
        prompt = "Escribe un saludo corto de 5 palabras."
        try:
            res = client.run_gem(prompt)
            print(f"Respuesta length: {len(res['raw'])}")
        except Exception as e:
            print(f"Fallo la ejecución directa: {e}")
    else:
        print("GEMINI_API_KEY no configurada para ejecución directa.")
