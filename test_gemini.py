import os
from dotenv import load_dotenv
from agent.gemini_client import GeminiClient

if __name__ == "__main__":
    load_dotenv()
    client = GeminiClient(api_key=os.getenv("GEMINI_API_KEY"), model="gemini-2.0-flash")
    prompt = "Escribe un saludo corto de 5 palabras."
    res = client.run_gem(prompt)
    print(f"Respuesta length: {len(res['raw'])}")
