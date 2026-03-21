import os
import sys
import asyncio

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.gemini_client import GeminiClient
from dotenv import load_dotenv

async def manual_test():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "dummy")
    client = GeminiClient(api_key=api_key, model="gemini-2.0-flash")
    prompt = "Escribe un saludo corto de 5 palabras."
    try:
        # GeminiClient.run_gem is now async
        res = await client.run_gem(prompt)
        print(f"Respuesta length: {len(res['raw'])}")
        return res
    except Exception as e:
        print(f"Test note: API call failed as expected or due to missing key: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(manual_test())
