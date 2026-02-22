import os
import sys
from dotenv import load_dotenv
from agent.gemini_client import GeminiClient

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment")
        return

    client = GeminiClient(api_key=api_key, model="gemini-2.5-flash")
    prompt = "Escribe un saludo corto de 5 palabras."
    res = client.run_gem(prompt)
    print(f"Respuesta length: {len(res['raw'])}")


if __name__ == "__main__":
    main()
