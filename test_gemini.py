import os
import sys

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv  # noqa: E402
from agent.gemini_client import GeminiClient  # noqa: E402

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY no detectada. Saltando prueba.")
        sys.exit(0)

    client = GeminiClient(api_key=api_key, model="gemini-2.0-flash")
    prompt = "Escribe un saludo corto de 5 palabras."
    try:
        res = client.run_gem(prompt)
        print(f"Respuesta length: {len(res['raw'])}")
    except Exception as e:
        print(f"Error ejecutando Gemini: {e}")
