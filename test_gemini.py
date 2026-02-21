from agent.gemini_client import GeminiClient
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_basic():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        import pytest
        pytest.skip("GEMINI_API_KEY not found")

    client = GeminiClient(api_key=api_key, model="gemini-2.5-flash")
    prompt = "Escribe un cuento corto de 100 palabras."
    res = client.run_gem(prompt)
    assert len(res['raw']) > 0
    print(f"Respuesta length: {len(res['raw'])}")

if __name__ == "__main__":
    try:
        test_gemini_basic()
    except Exception as e:
        print(f"Error: {e}")
