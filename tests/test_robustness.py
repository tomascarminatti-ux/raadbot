from agent.gemini_client import GeminiClient
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_json_cleaning():
    """Verifica que GeminiClient pueda limpiar JSONs malformados comunes."""
    client = GeminiClient(api_key="dummy")

    # Caso 1: JSON con coma final (un error común de LLMs)
    malformed_json = '{"name": "test", "score": 10,}'
    cleaned = client._parse_response(f"```json\n{malformed_json}\n```")
    assert cleaned["json"]["score"] == 10

    # Caso 2: JSON sin backticks (fallback)
    raw_json = '{"status": "ok"}'
    parsed = client._parse_response(raw_json)
    assert parsed["json"]["status"] == "ok"

    # Caso 3: JSON rodeado de texto
    mixed = "Aquí está el resultado:\n```json\n{\"val\": 1}\n```\nEspero que sirva."
    parsed_mixed = client._parse_response(mixed)
    assert parsed_mixed["json"]["val"] == 1
    assert "Aquí está el resultado" in parsed_mixed["markdown"]


if __name__ == "__main__":
    print("Corriendo tests de robustez de GeminiClient...")
    try:
        test_json_cleaning()
        print("✅ test_json_cleaning pasado")
        print("\n🎉 Todos los tests de robustez pasaron exitosamente.")
    except Exception as e:
        print(f"❌ Error en los tests: {e}")
        sys.exit(1)
