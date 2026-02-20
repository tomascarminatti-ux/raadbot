from agent.gemini_client import GeminiClient
import os
from dotenv import load_dotenv

load_dotenv()
client = GeminiClient(api_key=os.getenv("GEMINI_API_KEY"), model="gemini-2.5-flash")
prompt = "Escribe un cuento muy largo de 5000 palabras."
res = client.run_gem(prompt)
print(f"Respuesta length: {len(res['raw'])}")
