
## 2025-05-15 - Connection Pooling in GEMClient
**Learning:** Reusing a persistent httpx.AsyncClient session reduces network overhead by avoiding repeated TCP/TLS handshakes, especially beneficial for high-frequency internal API calls.
**Action:** Always prefer persistent sessions for internal clients managed via application lifecycle (e.g., FastAPI lifespan) to ensure proper initialization and closure.

## 2025-05-15 - Pytest collection error in test_gemini.py
**Learning:** Top-level network-bound logic in test files causes ============================= test session starts ==============================
platform linux -- Python 3.12.13, pytest-8.4.2, pluggy-1.6.0
rootdir: /app
configfile: pytest.ini
plugins: anyio-4.13.0, asyncio-0.23.6
asyncio: mode=Mode.AUTO
collected 4 items

tests/test_contracts.py ..                                               [ 50%]
tests/test_gem6.py .                                                     [ 75%]
tests/test_robustness.py .                                               [100%]

=============================== warnings summary ===============================
../home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/_pytest/config/__init__.py:1474
  /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/_pytest/config/__init__.py:1474: PytestConfigWarning: Unknown config option: asyncio_default_fixture_loop_scope

    self._warn_or_fail_if_strict(f"Unknown config option: {key}\n")

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
========================= 4 passed, 1 warning in 1.27s ========================= collection errors in environments without internet access or necessary services (like Ollama).
**Action:** Always wrap execution logic in standalone test scripts with  to prevent ============================= test session starts ==============================
platform linux -- Python 3.12.13, pytest-8.4.2, pluggy-1.6.0
rootdir: /app
configfile: pytest.ini
plugins: anyio-4.13.0, asyncio-0.23.6
asyncio: mode=Mode.AUTO
collected 4 items

tests/test_contracts.py ..                                               [ 50%]
tests/test_gem6.py .                                                     [ 75%]
tests/test_robustness.py .                                               [100%]

=============================== warnings summary ===============================
../home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/_pytest/config/__init__.py:1474
  /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/_pytest/config/__init__.py:1474: PytestConfigWarning: Unknown config option: asyncio_default_fixture_loop_scope

    self._warn_or_fail_if_strict(f"Unknown config option: {key}\n")

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
========================= 4 passed, 1 warning in 1.46s ========================= from running it during discovery.

## 2025-05-15 - Pytest collection error in test_gemini.py
**Learning:** Top-level network-bound logic in test files causes pytest collection errors in environments without internet access or necessary services (like Ollama).
**Action:** Always wrap execution logic in standalone test scripts with if __name__ == "__main__": to prevent pytest from running it during discovery.
