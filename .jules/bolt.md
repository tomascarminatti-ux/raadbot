## 2025-05-15 - Optimizing Prompt Construction with Caching
**Learning:** Prompt templates are static assets that are frequently read from disk. Using `functools.lru_cache` for I/O operations and pre-compiling regular expressions for variable replacement significantly reduces overhead in the critical path of prompt generation.
**Action:** Always consider `@lru_cache` for static file reads and move regex compilation/expensive imports to the module level.
