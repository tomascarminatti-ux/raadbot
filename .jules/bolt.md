## 2025-05-22 - [Optimization of Prompt Construction]
**Learning:** Caching static prompt templates with `lru_cache` and using `re.sub` with a callback for variable injection provides a massive performance boost (70x+) over redundant disk I/O and repeated `.replace()` calls. Storing per-run state on a shared orchestrator instance is an anti-pattern that introduces race conditions in concurrent environments.
**Action:** Always use `lru_cache` for file-based templates and keep orchestrator instances stateless or use a thread-safe context manager for per-run data. Focus on ONE high-impact optimization at a time to maintain code quality and safety.

## 2026-02-22 - [CI Failure Prevention]
**Learning:** Script files named `test_*.py` are collected by pytest and executed if they have top-level calls. This can fail CI if they depend on environment variables (like API keys) that are missing.
**Action:** Always wrap script logic in `if __name__ == "__main__":` and follow PEP 8 linting rules strictly (e.g., imports at top) to ensure CI compatibility.
