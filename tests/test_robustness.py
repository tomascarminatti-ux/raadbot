import sys
import os
import json

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.gemini_client import GeminiClient
from agent.pipeline import Pipeline

def test_json_cleaning():
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

def test_gem_normalization():
    # Mocking basic setup
    pipeline = Pipeline(gemini=None, search_id="test", output_dir="temp_test")
    
    assert pipeline._normalize_gem_name("GEM1") == "gem1"
    assert pipeline._normalize_gem_name("GEM_1") == "gem1"
    assert pipeline._normalize_gem_name("gem-1") == "gem1"
    assert pipeline._normalize_gem_name("GEM_5") == "gem5"
    
    # Limpiar temp dir
    import shutil
    if os.path.exists("temp_test"):
        shutil.rmtree("temp_test")

if __name__ == "__main__":
    print("Corriendo tests de robustez...")
    try:
        test_json_cleaning()
        print("✅ test_json_cleaning pasado")
        test_gem_normalization()
        print("✅ test_gem_normalization pasado")
        print("\n🎉 Todos los tests pasaron exitosamente.")
    except Exception as e:
        print(f"❌ Error en los tests: {e}")
        sys.exit(1)
