import os
import sys

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.gemini_client import GeminiClient
from dotenv import load_dotenv

def test_placeholder():
    # This file causes CI failures because it tries to connect to Ollama/Gemini during collection
    # We keep it for manual testing but disable its execution by pytest
    pass

if __name__ == "__main__":
    load_dotenv()
    # Check if we have an API key or a local Ollama before running
    if not os.getenv("GEMINI_API_KEY") and os.getenv("LLM_PROVIDER") != "ollama":
        print("Skipping manual test: No GEMINI_API_KEY and provider is not ollama")
        sys.exit(0)

    client = GeminiClient(api_key=os.getenv("GEMINI_API_KEY"), model="gemini-2.5-flash")
    prompt = "Escribe un saludo corto de 5 palabras."
    try:
        res = client.run_gem(prompt)
        print(f"Respuesta length: {len(res['raw'])}")
    except Exception as e:
        print(f"Error running gem: {e}")
