## 2025-05-14 - Prompt Template Memoization
**Learning:** In a multi-agent system where prompts are built dynamically for each candidate, repeated disk I/O for static templates (especially a shared "maestro" prompt) becomes a significant bottleneck during parallel processing. Moving `json` imports from function scope to module scope also yields a minor but measurable reduction in overhead.
**Action:** Always use `@functools.lru_cache` for functions that load static resources like prompt templates or schemas.
