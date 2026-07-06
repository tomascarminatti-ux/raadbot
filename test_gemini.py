import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def run_verify():
    # Import GeminiClient inside the function to avoid any import-time execution issues
    from agent.gemini_client import GeminiClient
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    client = GeminiClient(api_key=api_key, model="gemini-2.0-flash")
    prompt = "Escribe un saludo corto de 5 palabras."
    try:
        res = client.run_gem(prompt)
        print(f"Respuesta length: {len(res['raw'])}")
    except Exception as e:
        print(f"Error running gem: {e}")


if __name__ == "__main__":
    run_verify()
