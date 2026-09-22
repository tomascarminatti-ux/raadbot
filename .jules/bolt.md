# Bolt's Journal - Critical Performance Learnings

## Architectural Bottlenecks & Patterns

* In `agent/prompt_builder.py`, template loading benefits significantly from `@functools.lru_cache(maxsize=32)` using file `mtime` for cache invalidation.
* In `agent/gemini_client.py` and `agent/prompt_builder.py`, pre-compiling regular expressions as module-level constants avoids repeated regex string parsing.
* In `utils/gem_core.py`, contract schema caching using `@functools.lru_cache` keyed by path and file mtime eliminates disk read overhead during repeated contract validation.
* In `utils/gem_core.py`, reusing a persistent `httpx.AsyncClient` session in `GEMClient` avoids per-request connection overhead.
* In `utils/input_loader.py`, cached file reading using `@functools.lru_cache` keyed by path and mtime speeds up local input loading.
