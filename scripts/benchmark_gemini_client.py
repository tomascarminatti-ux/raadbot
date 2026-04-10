import time
import os
import sys
sys.path.append(os.getcwd())
from agent.gemini_client import GeminiClient

def benchmark_parse():
    client = GeminiClient(api_key="dummy")
    raw_text = """
He analizado el candidato. Aquí está el resultado en JSON:

```json
{
  "thought": "El candidato tiene buena experiencia en Python.",
  "action": "call_agent",
  "agent_id": "gem2",
  "payload": {"data": "..."}
}
```

Espero que esto sea útil.
"""

    start = time.perf_counter()
    for _ in range(1000):
        client._parse_response(raw_text)
    end = time.perf_counter()

    avg_time = (end - start) / 1000 * 1000
    print(f"Average _parse_response time: {avg_time:.4f} ms")

if __name__ == "__main__":
    benchmark_parse()
