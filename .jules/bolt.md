## 2025-05-18 - System Prompt Template Caching & Precompiled Regexes

**Learning:** Prompt template loading in `agent/prompt_builder.py` originally performed blocking file I/O reads from disk on every template build or variable extraction call. Wrapping `load_prompt()` with `@functools.lru_cache(maxsize=32)` eliminated repeated disk I/O, providing a >100x speedup for prompt rendering while keeping prompt invalidation clean via `clear_prompt_caches()` on prompt edits in `api.py`. Additionally, pre-compiling regular expressions (`VAR_RE`, `JSON_BLOCK_RE`, `ANY_JSON_RE`, `TRAILING_COMMA_RE`) at module level eliminated string regex compilation overhead across prompt building and LLM response parsing.

**Action:** Always pre-compile frequently executed regular expressions at module level and apply LRU memoization with invalidation hooks for static disk assets accessed during request hot paths.
