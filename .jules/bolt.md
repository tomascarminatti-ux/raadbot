## 2026-02-25 - Prompt Template Loading LRU Caching with File Modification Timestamp Invalidation

**Learning:** Prompt template file reads and response regex parsing were repeatedly executing during agent prompt construction and Gemini/Ollama response parsing. By using `@functools.lru_cache` on file path + modification timestamp (`mtime`), we avoid disk I/O on repeated reads while ensuring automatic cache invalidation when prompt files are modified on disk. Pre-compiling module-level regex constants further eliminates regex compilation overhead per response parsing call.
**Action:** Always wrap file read operations in a cached helper function keyed on `(filepath, mtime)` when templates or JSON schemas are repeatedly read during agent executions.
