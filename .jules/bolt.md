
## 2025-05-15 - Connection Pooling in GEMClient
**Learning:** Reusing a persistent httpx.AsyncClient session reduces network overhead by avoiding repeated TCP/TLS handshakes, especially beneficial for high-frequency internal API calls.
**Action:** Always prefer persistent sessions for internal clients managed via application lifecycle (e.g., FastAPI lifespan) to ensure proper initialization and closure.

## 2025-05-15 - Pytest collection error in test_gemini.py
**Learning:** Top-level network-bound logic in test files causes pytest collection errors in environments without internet access or necessary services (like Ollama).
**Action:** Always wrap execution logic in standalone test scripts with `if __name__ == "__main__":` to prevent pytest from running it during discovery.
