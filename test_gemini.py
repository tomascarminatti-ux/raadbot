import os
import sys
import asyncio
from dotenv import load_dotenv

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from agent.gemini_client import GeminiClient  # noqa: E402


async def run_test():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    async with GeminiClient(api_key=api_key, model="gemini-2.5-flash") as client:
        prompt = "Escribe un saludo corto de 5 palabras."
        try:
            res = await client.run_gem(prompt)
            print(f"Respuesta length: {len(res['raw'])}")
        except Exception as e:
            print(f"Test skipped or failed: {e}")


if __name__ == "__main__":
    asyncio.run(run_test())
