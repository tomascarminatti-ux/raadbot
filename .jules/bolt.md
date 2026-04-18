## 2025-05-15 - [Initial Profiling]
**Learning:** Identified two major performance bottlenecks in the current architecture:
1. `GEMClient` (used for DB interactions) creates a new `httpx.AsyncClient` for every single request. This adds ~50ms of overhead per call due to connection establishment.
2. `prompt_builder.py` reads system prompts and the maestro prompt from disk on every `build_prompt` call. While disk I/O is fast, it's redundant for static templates.
3. `api.py` uses inline imports in hot paths (like GEM 5 setup) which adds unnecessary overhead.
4. `GEM6Orchestrator.run_pipeline` uses `time` but doesn't import it, which will cause a runtime crash.

**Action:**
1. Implement connection pooling in `GEMClient` using a persistent client.
2. Add `@lru_cache` to `prompt_builder` template loading functions.
3. Move inline imports to top-level in `api.py`.
4. Fix missing imports and implement proper resource cleanup (aclose) across the stack.
