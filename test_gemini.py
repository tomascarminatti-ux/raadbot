import os
import sys
import asyncio
from dotenv import load_dotenv

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.gemini_client import GeminiClient

async def manual_test_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Skipping manual_test_gemini: No GEMINI_API_KEY found.")
        return

    client = GeminiClient(api_key=api_key, model="gemini-2.5-flash")
    prompt = "Escribe un saludo corto de 5 palabras."
    res = await client.run_gem(prompt)
    print(f"Respuesta length: {len(res['raw'])}")

if __name__ == "__main__":
    asyncio.run(manual_test_gemini())
