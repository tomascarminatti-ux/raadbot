import os
import sys

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.gemini_client import GeminiClient
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        client = GeminiClient(api_key=api_key, model="gemini-2.5-flash")
        prompt = "Escribe un saludo corto de 5 palabras."
        try:
            res = client.run_gem(prompt)
            print(f"Respuesta length: {len(res['raw'])}")
        except Exception as e:
            print(f"Error running gemini client: {e}")
    else:
        print("GEMINI_API_KEY not found, skipping execution.")
