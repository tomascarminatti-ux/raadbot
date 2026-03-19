import os
import sys

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.gemini_client import GeminiClient
from dotenv import load_dotenv

load_dotenv()

def manual_test_gemini():
    client = GeminiClient(api_key=os.getenv("GEMINI_API_KEY"), model="gemini-2.5-flash")
    prompt = "Escribe un saludo corto de 5 palabras."
    try:
        res = client.run_gem(prompt)
        print(f"Respuesta length: {len(res['raw'])}")
    except Exception as e:
        print(f"Manual test failed (expected if no API key/Ollama): {e}")

if __name__ == "__main__":
    manual_test_gemini()
